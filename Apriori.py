def readData(fileName):
    TDB = dict();
    items = [];
    C1 = set();
    with open(fileName, "r") as file:
        for line in file.readlines():
            data = line.strip().split();
            # for IBM
            for i in range(len(data)):
                data[i] = int(data[i]);
            if(TDB.get(data[1])):
                TDB[data[1]].append(data[2]);
            else:
                TDB[data[1]] = [data[2]];
            C1.add(frozenset({data[2]}));
    for values in TDB.values():
        items.append(set(values));
    return [items, C1];


def createFk(items, Ck, minSupport):
    Fk = set();
    supportData = dict();
    for i in Ck:
        sup = 0;
        for item in items:
            if(i.issubset(item)):
                sup += 1;
        if((sup / len(items)) >= minSupport):
            Fk.add(i);
            supportData[i] = sup / len(items);
    return [Fk, supportData];


def createCk(Fk, Cksub):
    Ck = set();
    Fk_list = list(Fk);
    for i in range(len(Fk_list)):
        for j in range(i + 1, len(Fk_list)):
            tmpUnionSet = Fk_list[i].union(Fk_list[j]);
            # prune when the abandoned set's is the tmpUnionSet's subset
            prune = False;
            for disuse in (Cksub - Fk):
                if(disuse.issubset(tmpUnionSet)):
                    prune = True;
            if(not prune):
                Ck.add(tmpUnionSet);
    return Ck;


def apriori(items, Ck, minSupport):
    global supportData;
    Fk = createFk(items, Ck, minSupport);
    if(len(Fk[0]) > 0):
        for freq_item, sup in Fk[1].items():
            try:
                supportData[len(freq_item)].update({freq_item:sup});
            except:
                supportData[len(freq_item)] = {freq_item:sup};
        CkNext = createCk(Fk[0], Ck);
        apriori(items, CkNext, minSupport);


def generateRules(supportData, minConfidence):
    rules = [];
    setDict = dict();
    for freq_items in supportData.values():
        for freq_item, sup in freq_items.items():
            for set in setDict.keys():
                if(set.issubset(freq_item)):
                    confidence = sup / setDict[set];
                    rule = (set, freq_item - set, confidence);
                    if(confidence >= minConfidence and (rule not in rules)):
                        rules.append(rule);
        setDict.update(freq_items);
    return rules;

        
if __name__ == '__main__':
    # init
    dataFile = "data.txt";
    # dataFile = "winequalityN.txt";
    minSupport = 0.025;
    minConfidence = 0.8;
    ''' supportData
    { 1 : { set(): sup, set(): sup,... }, 
      2 : {}, 
      3 : {}, 
    ...}
    '''
    supportData = dict();
    # read data
    ''' Read the data.txt and then set the data format like:
        items = {{A,B,C},{B,C,D},...}
        i1 = { {A},{B},{C},...}
    '''
    Data = readData(dataFile);
    # Data = readData("winequalityN.txt");
    items = Data[0];  # each Tid's set
    C1 = Data[1];  # candidat_1
    # apriori algo.
    apriori(items, C1, minSupport);
    
    # print frequent-items & support 
    for k, freq_items in supportData.items():
        print("="*50);
        print("frequent ", k , "-itemsets\tsupport")
        print("="*50);
        for freq_item, sup in freq_items.items():
            print(list(freq_item), "\t", sup);
            
    # generate association rules
    print("Association rules:");
    for rule in generateRules(supportData, minConfidence):
        print(list(rule[0]), "=>", list(rule[1]), "confidence", rule[2]);