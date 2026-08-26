import sys

from app.graph.workflow import graph


def get_paper_text():
    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/paper.txt")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


paper_text = get_paper_text()

initial_state = {
    "paper_text": paper_text,
    "analysis": "",
    "plan": "",
    "generated_code": "",
    "execution_result": "",
    "critique": "",
    "retry_count": 0,
    "evaluation": "",
    "status": ""
}


result = graph.invoke(initial_state)


print("\nANALYSIS:")
print(result["analysis"])

print("\nPLAN:")
print(result["plan"])

print("\nGENERATED CODE:")
print(result["generated_code"])

print("\nEXECUTION RESULT:")
print(result["execution_result"])

print("\nCRITIQUE:")
print(result["critique"])

print("\nRETRY COUNT:")
print(result["retry_count"])

print("\nEVALUATION:")
print(result["evaluation"])

print("\nSTATUS:")
print(result["status"])