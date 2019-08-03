from newsExtracter import Extracter

extracter=Extracter()
extracter.createClassModel()
# extracter.createSubjectModel()
# extracter.createNTripleModel()
print("Input Text")
# result=extracter.extractClass("金蝶纯利增长达34%创四年同期新高")
while True:
    print(extracter.extractClass(input()))
