import subprocess
import sys
import tempfile
import os


def execute_code(state):
    code = state["generated_code"]

    if not code:
        return {
            "execution_result": "No code was generated.",
            "status": "failed"
        }

    temp_file = None

    try:
        # Create temporary Python file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_file = f.name

        # -------------------------------------------------
        # STEP 1: Syntax validation
        # -------------------------------------------------
        syntax_check = subprocess.run(
            [sys.executable, "-m", "py_compile", temp_file],
            capture_output=True,
            text=True
        )

        if syntax_check.returncode != 0:
            execution_result = (
                f"SYNTAX VALIDATION FAILED:\n"
                f"{syntax_check.stderr}\n\n"
                f"RETURN CODE: {syntax_check.returncode}"
            )

            return {
                "execution_result": execution_result,
                "status": "failed"
            }

        # -------------------------------------------------
        # STEP 2: Runtime execution
        # -------------------------------------------------
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=60
        )

        execution_result = (
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}\n\n"
            f"RETURN CODE: {result.returncode}"
        )

        if result.returncode == 0:
            status = "success"
        else:
            status = "failed"

        return {
            "execution_result": execution_result,
            "status": status
        }

    except subprocess.TimeoutExpired:
        return {
            "execution_result": "Execution timed out after 60 seconds.",
            "status": "failed"
        }

    except Exception as e:
        return {
            "execution_result": f"Executor error: {str(e)}",
            "status": "failed"
        }

    finally:
        # Delete temporary file
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)