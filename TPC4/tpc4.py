import re
import json
from statistics import mean


def parse_header(line):
    header_regex = re.compile(r"([^,{]+)(?:\{(\d+)(?:,(\d+))?\}(?:::(\w+))?)?[,]?")
    header_info = header_regex.findall(line.strip())

    header = []
    lists = dict()
    totals = dict()
    for name, qta, qtb, total in header_info:
        header.append(name)

        if total != '':
            lists[name] = (int(qta), int(qtb) if qtb else '')
            totals[name] = total
        elif qta != '':
            lists[name] = (int(qta), int(qtb) if qtb else '')

    return header, lists, totals


def parse_data(lines, header, lists, totals):
    rest_regex = ""
    for name in header:
        if name in lists:
            qta, qtb = lists[name]
            qtd = f"{{{qta},{qtb}}}" if qtb else f"{{{qta}}}"
            rest_regex += rf"(?P<{name}>([^,]+[,]?){qtd})[,]?"
        else:
            rest_regex += rf"(?P<{name}>[^,]+)[,]?"

    rest_regex = re.compile(rest_regex)

    data = [match.groupdict() for line in lines[1:] for match in rest_regex.finditer(line.strip())]

    for elem in data:
        for name in header:
            if name in lists:
                elem[name] = [int(num) for num in re.findall(r"\d+", elem[name])]
            if name in totals:
                if totals[name] == "sum":
                    elem[name] = sum(elem[name])
                elif totals[name] == "media":
                    elem[name] = mean(elem[name])

    return data


def main():
    with open("alunos5.csv") as file:
        lines = file.readlines()

    header, lists, totals = parse_header(lines[0])

    data = parse_data(lines, header, lists, totals)

    with open("alunos5.json", "w") as json_file:
        json.dump(data, json_file, indent=len(header), ensure_ascii=False)


if __name__ == '__main__':
    main()
