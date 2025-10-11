class Student {
  name: string;
  rollNo: number;
  marks: number;

  constructor(name: string, rollNo: number, marks: number) {
    this.name = name;
    this.rollNo = rollNo;
    this.marks = marks;
  }

  grade(): string {
    if (this.marks >= 90) return "A+";
    else if (this.marks >= 75) return "A";
    else if (this.marks >= 60) return "B";
    else return "C";
  }

  display(): void {
    console.log(`Name: ${this.name}, Roll: ${this.rollNo}, Grade: ${this.grade()}`);
  }
}

const s1 = new Student("Akshay", 101, 88);
s1.display();
