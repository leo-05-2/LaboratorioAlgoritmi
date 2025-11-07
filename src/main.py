from src.Tester import *

if __name__ == "__main__":
    tester = StructureTester()
    tester.run_tests()
    tester.plot_results(False)
    tester.plot_results(True)
    tester.plot_results(True,['LinkedList', 'SBStree'])
    tester.plot_results(True,['LinkedList', 'BSTree'])
    tester.run_tests(True)
    tester.plot_results(True, ['LinkedList', 'SBStree'])
    tester.plot_results(True, ['LinkedList', 'BSTree'])



