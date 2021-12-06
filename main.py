import os

from typing import Union


class Parser(object):
    def __init__(self, input_file, output_file):
        os.makedirs("tmp", exist_ok=True)
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        st, mes = self.read_and_operate("order")
        if not st:
            return "FAILED!!! " + mes
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        st, mes = self.read_and_operate("gen_output")
        if not st:
            mes = "FAILED!!! " + mes
        return mes

    def read_and_operate(self, op: str = "order"):
        if op not in ["order", "gen_output"]:
            return False, "Wrong value of 'op', need to be one of 'order', 'gen_output'"
        if op == "order":
            with open(self.input_file, "r") as f:
                for line in f:
                    if line:
                        self.write_rec(*line.split(","))
        elif op == "gen_output":
            self.create_output()
        return True, "success"

    @staticmethod
    def write_rec(
            department: str,
            date: str,
            amount: Union[int, str],
    ):
        if isinstance(amount, str):
            amount = int(amount)
        if os.path.exists(os.path.join("tmp/", department)):
            with open(os.path.join("tmp/", department), "r") as f:
                try:
                    amount += int(f.read())
                except ValueError:
                    pass

        with open(os.path.join("tmp/", department), "w") as f:
            f.write(str(amount))

    def create_output(self):
        for department in os.listdir("tmp"):
            with open(os.path.join("tmp/", department)) as f:
                amount = f.read()
            with open(self.output_file, "a") as f:
                f.write(f"{department},{amount}\n")
            os.remove(os.path.join("tmp/", department))


parser = Parser("input", "output")
parser.run()
