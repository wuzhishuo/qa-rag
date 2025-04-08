from app.vector_db import build_vector_db

if __name__ == "__main__":
    print("🚀 正在构建向量库...")
    build_vector_db("data/help_center.txt")
    print("✅ 向量库构建完成，已保存到 vector_db/")
