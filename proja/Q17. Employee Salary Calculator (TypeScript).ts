class Employee {
  name: string;
  basicPay: number;
  hra: number;
  deductions: number;

  constructor(name: string, basic: number, hra: number, ded: number) {
    this.name = name;
    this.basicPay = basic;
    this.hra = hra;
    this.deductions = ded;
  }

  calculateSalary(): number {
    return this.basicPay + this.hra - this.deductions;
  }

  display(): void {
    console.log(`Employee: ${this.name}, Net Salary: ₹${this.calculateSalary()}`);
  }
}

const emp1 = new Employee("John", 30000, 8000, 2000);
emp1.display();
