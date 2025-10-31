from src.Tester import *

if __name__ == "__main__":
    tester = StructureTester()
    #rs,rr=tester.run_simple_test()
    #tester.plot_simple_result(rs,rr)
    rs,rr=tester.run_balanced_vs_list()
    tester.plot_balanced_vs_list(rs,rr)

