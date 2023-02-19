from prettytable import PrettyTable


def parse(myheart: str):
    struct = []
    with open(myheart, "r") as content:
        fstline = content.readline().strip().split(",")
        
        for line in content:
            row={}
            data = line.rstrip().split(",")

            for a in range(len(fstline)):
                row[fstline[a]] = data[a]

            struct.append(row)

    return struct


def distribuicaoPorSexo (struct:list[object]):
  generos={'Masculino com doença':0, 'Feminino com doença':0}

  for dataset in struct:
    if dataset.get('temDoença')=='1':
      if dataset['sexo']=='M':
        generos['Masculino com doença']+=1
      elif dataset['sexo']=='F':
        generos['Feminino com doença']+=1
      else:
        print ('Error')
  return generos


def distribuicaoPorIdade (struct):
    idades=[]
    for dataset in struct:
        idades.append(int(dataset['idade']))
    idadeMax=max(idades)


    idadeRanges={}
    for a in range(30, idadeMax,4):
        idadeRanges[f"{a}-{a+4}"]=0

    for dataset in struct:
        idade=int(dataset['idade'])
        for intervalo in idadeRanges:
            i,f=map(int, intervalo.split("-"))
            if i<=idade<=f and dataset['temDoença']=='1':
                idadeRanges[intervalo]+=1

    return idadeRanges

def distribuicaoPorColesterol(struct):
    col=[]
    for dataset in struct:
        col.append(int(dataset['colesterol']))
    

    colMin=min(col)
    colMax=max(col)

    colRanges={}
    for c in range(colMin,colMax,10):
        colRanges[f"{c}-{c+10}"]=0

    for dataset in struct:
        colest=int(dataset['colesterol'])
        for intervalo in colRanges:
            i,f=map(int, intervalo.split("-"))
            if i<=colest<=f and dataset['temDoença']=='1':
                colRanges[intervalo]+=1


    return colRanges

def tabelaDist(dic: dict, subject: str):

    table = PrettyTable(["Intervalo", subject])

    for content, number in dic.items():
        table.add_row([content, number])

    return table


def selectDistributions(data):
    subject: str
    selecao= 1
    while (selecao != 0):
        selecao = int(input(
            "Selecione a distribuicao:\n1 - Por sexo\n2 - Por idade\n3 - Por colesterol\n"))
        if selecao != 0:
            if selecao == 1:
                subject = "Sexo"
                print(tabelaDist(distribuicaoPorSexo(data),subject))
                break
                
            elif selecao == 2:
                subject = "Idade"
                print(tabelaDist(distribuicaoPorIdade(data),subject))
                break
                
            elif selecao == 3:
                subject = "Colesterol"
                print(tabelaDist(distribuicaoPorColesterol(data),subject))
                break
                
            else:
                print("Error")
                break


def main():
    data=parse("myheart.csv")
    selectDistributions(data)


main()    


