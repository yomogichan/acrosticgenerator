import unittest
import acrosticgenerator as ag
import util

class TestStringMethods(unittest.TestCase):
    def start_with(self, in_word,theme,end,filename):
        final_list = ag.final_output(in_word,theme, end, filename)
        result = []
        for sent in final_list:
            result.append(sent[0].lower())
        result = "".join(result)
        assert result == in_word


    def test_start_with(self):
        """
        Unit test checks the beginning of the sentence
        """
        self.start_with("missyou","I love you",False,"testsample.txt")

    def check_remove_punct(self, in_str, out_str):
        result = util.remove_end_punct(in_str)
        assert result == out_str

    def test_remove_punct(self):
        """
        Unit test checks the remove punctuation function.
        """
        self.check_remove_punct("I hate human!", "I hate human")
        self.check_remove_punct("", "")
        self.check_remove_punct(" ", "")
        self.check_remove_punct(".!::", "")
        self.check_remove_punct("häää!?!", "häää")
        self.check_remove_punct("hello:!", "hello")
        self.check_remove_punct("a", "a")
        self.check_remove_punct("hmmm ?", "hmmm")


    def check_output_format(self, in_str, out_str, end = False):
        result = util.output_format(in_str, end)
        assert result == out_str


    def test_output_format(self):
        """
        Unit test checks the output format.
        """
        self.check_output_format("","")
        self.check_output_format(" "," ")
        self.check_output_format("aoiejfao","Aoiejfao")
        self.check_output_format("Hiii","hiiI",True)
        self.check_output_format(",.?!",",.?!",True)

if __name__ == '__main__':
    unittest.main()

