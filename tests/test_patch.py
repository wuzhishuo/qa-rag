import requests
import json
import time

API_URL = "http://localhost:8000/qa"
TEST_FILE = "tests/test_queries.jsonl"

def run_tests():
    session_history = []

    with open(TEST_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            item = json.loads(line.strip())
            query = item["query"]

            payload = {
                "query": query,
                "history": session_history
            }

            print(f"\n🟡 发送问题 {i}: {query}")
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                answer = response.json()["answer"]
                print(f"🟢 回答: {answer}")
                session_history.append(query)
            else:
                print(f"🔴 请求失败: {response.status_code} - {response.text}")
            
            time.sleep(1)  # 避免请求太快触发限流

if __name__ == "__main__":
    run_tests()
