#!/usr/bin/env python3
"""
Text-to-SQL E-commerce Platform

Usage:
    python run.py demo    # Interactive demo
    python run.py api     # Launch API server
    python run.py eval    # Run evaluation
"""

import argparse


def demo():
    """Interactive demo."""
    from src.sql.generator import generate_sql
    from src.sql.executor import execute_sql, get_connection
    
    print("=" * 60)
    print("TEXT-TO-SQL DEMO")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    conn = get_connection()
    
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in ["quit", "exit", "q"]:
            break
        
        sql = generate_sql(question)
        print(f"\nSQL: {sql}")
        
        success, result, error = execute_sql(sql, conn)
        if success:
            print(f"\nResult:\n{result}")
        else:
            print(f"\nError: {error}")
    
    conn.close()
    print("\nBye!")


def api():
    """Launch API server."""
    import uvicorn
    print("=" * 60)
    print("TEXT-TO-SQL API")
    print("=" * 60)
    print("URL: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)


def evaluate():
    """Run evaluation."""
    import json
    from src.sql.generator import generate_sql
    from src.sql.executor import execute_sql, get_connection
    from src.evaluation.metrics import execution_accuracy
    
    print("=" * 60)
    print("EVALUATION")
    print("=" * 60)
    
    with open("data/results/test_questions.json", "r") as f:
        questions = json.load(f)
    
    conn = get_connection()
    correct = 0
    total = len(questions)
    
    by_difficulty = {"simple": [0, 0], "medium": [0, 0], "complex": [0, 0]}
    
    for i, q in enumerate(questions):
        sql = generate_sql(q["question"])
        gen_ok, gen_res, _ = execute_sql(sql, conn)
        exp_ok, exp_res, _ = execute_sql(q["sql"], conn)
        
        ex = execution_accuracy(gen_res, exp_res) if gen_ok and exp_ok else False
        if ex:
            correct += 1
            by_difficulty[q["difficulty"]][0] += 1
        by_difficulty[q["difficulty"]][1] += 1
        
        status = "[OK]" if ex else "[FAIL]"
        print(f"[{i+1:2d}] {status} [{q['difficulty']:7s}] {q['question'][:40]}...")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Execution Accuracy: {correct}/{total} ({correct/total:.0%})")
    print("\nBy difficulty:")
    for diff, (ok, tot) in by_difficulty.items():
        print(f"  {diff:8s}: {ok}/{tot} ({ok/tot:.0%})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text-to-SQL Platform")
    parser.add_argument("command", choices=["demo", "api", "eval"])
    args = parser.parse_args()
    
    if args.command == "demo":
        demo()
    elif args.command == "api":
        api()
    elif args.command == "eval":
        evaluate()
