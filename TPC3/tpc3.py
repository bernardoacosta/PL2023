import json
import re


def yearly(data):
    procs = dict()

    for proc in data:
        year = proc["year"]
        if year not in procs:
            procs[year] = 1
        else:
            procs[year] += 1

    return procs


def nomes_sec(data):
    fstnames = dict()
    lstnames = dict()
    
    for proc in data:
        first_name = re.match(r"\b[A-Za-z]+\b", proc["name"]).group()
        last_name = re.search(r"\b[A-Za-z]+$", proc["name"]).group()
        year = proc["year"]
        sec = (int(year) // 100) + 1

        if sec not in fstnames:
            fstnames[sec] = dict()

        if sec not in lstnames:
            lstnames[sec] = dict()
        
        if first_name not in fstnames[sec]:
            fstnames[sec][first_name] = 0
        
        if last_name not in lstnames[sec]:
            lstnames[sec][last_name] = 0

        fstnames[sec][first_name] += 1
        lstnames[sec][last_name] += 1

    return fstnames, lstnames



def prtnames(fstnames, lstnames):
    fstnamekeys = list(fstnames.keys())
    fstnamekeys.sort()
    lstnamekeys = list(lstnames.keys())
    lstnamekeys.sort()
    
    print("Nomes Proprios")

    for sec in fstnamekeys:
        print("Seculo " + str(sec))

        items = list(fstnames[sec].items())
        items.sort(key=lambda x : x[1], reverse=True)

        for i in range(0, 5):
            print(items[i])

    print("Apelidos")

    for sec in lstnamekeys:
        print("Seculo " + str(sec))

        items = list(lstnames[sec].items())
        items.sort(key=lambda x : x[1], reverse=True)

        for i in range(0, 5):
            print(items[i])

def relacoes(data):
    relationship = dict()
    exp = re.compile(r"[a-zA-Z ]*,([a-zA-Z\s]*)\.[ ]*Proc\.\d+\.")

    for proc in data:
        obs = proc["obs"]
        matches = exp.finditer(obs)

        for match in matches:
            if match.group(1) not in relationship:
                relationship[match.group(1)] = 0
            relationship[match.group(1)] += 1
    
    return relationship

def ptjson(data, path):
    file = open(path + ".json", "w")
    json.dump(data[:20], file)

def dictionary(dict):
    for key in dict.keys():
        print(key + ' '*(20-len(key)) + "| " + str(dict[key]))


def main():
    ficheiro = open("processos.txt")
    regex = re.compile(r"(?P<folder>\d+)::(?P<year>\d{4})\-(?P<month>\d{2})-(?P<day>\d{2})::(?P<name>[A-Za-z ]+)::(?P<f_name>[A-Za-z ]+)::(?P<m_name>[A-Za-z ]+)::(?P<obs>.*)::")
    matches = regex.finditer(ficheiro.read()) 
    regex_obs = re.compile(r"Doc.danificado.")
    procs = dict()
    valids = list()

    for match in matches:
        if not regex_obs.search(match.group("obs")):
            if match.group("folder") in procs:
                if match.groupdict() not in procs[match.group("folder")]:
                    procs[match.group("folder")].append(match.groupdict())
            else:
                procs[match.group("folder")] = [match.groupdict()]
    
    for value in procs.values():
        valids += value

    option = 0
    while option != 5:
        print("1 - Frequencia de processos por ano")
        print("2 - Frequencia de nomes por seculo")
        print("3 - Frequencia de tipos de relacao")
        print("4 - 20 primeiros registos para json")
        print("5 - Sair")

        option = int(input())

        if(option==1):
            dictionary(yearly(valids))
        elif(option==2):
            fstnames, lstnames = nomes_sec(valids)
            prtnames(fstnames, lstnames)
        elif(option==3):
            dictionary(relacoes(valids))
        elif(option==4):
            ptjson(valids, "data")
if __name__ == '__main__':
    main()