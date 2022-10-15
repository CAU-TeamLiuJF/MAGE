'''
Description:
Author: Zhuo Yue
Date: 2021-06-16 22:56:30
LastEditors: zhuoy
LastEditTime: 2022-04-13 18:38:52
Calls:
Called By:
FilePath: \CCPMatrix\src\pedigree.py
'''


def AnalyzePedigree(filename_pedigree, filename_generation, tmp_prefix):
    # Organize pedigree files, complete individuals, calculate generations, write files by breeds
    import os
    import copy
    print("Start analyzing pedigree.\n")
    header = ['id', 'sire', 'dam', 'generations', 'breed']
    # Read pedigree files
    pedigree, breed, error_line = _ReadPedigree(filename_pedigree, header)
    # Line error in pedigree, termination
    if error_line:
        print('Error in pedigree file:\n')
        for line in error_line:
            print("{0}\n".format(line))
        return "2"
    # Complement the pedigree, any individual has one item
    pedigree = _AddIdv(pedigree, header)
    # Calculation Generation
    for idv in pedigree:
        pedigree = _CalculationGeneration(pedigree, idv)
    breed = dict(zip(breed, [0] * len(breed)))
    for i in breed:
        breed[i] = dict()
    # input purebred id into dictionary
    breed = _SplitPedigree(pedigree, breed)
    output_file_list = ["0", str(len(breed))]
    # Deal with the generation file
    tmp_file_gene_id = "{0}_gene_id".format(tmp_prefix)
    os.system("awk \'{0}\' {1} > {2}".format(
        "{print $1}", filename_generation, tmp_file_gene_id))
    with open(tmp_file_gene_id) as f:
        gene_id = [[x.rstrip('\n')] for x in f.readlines()]
    for i in range(len(gene_id)):
        gene_id[i].append(str(i + 1))
    pedigree_all = copy.deepcopy(pedigree)  # dominance need it
    breed_list = []
    for f_breed in breed:
        # Traverse the breed, and output file
        print("Start analyzing pedigree of breed {0}.\n".format(f_breed))
        gene_id_breed = copy.deepcopy(gene_id)
        # renumber
        output_file_list_breed = [f_breed]
        breed_list.append(f_breed)
        single_breed = breed.get(f_breed)
        single_breed, id_list = _ReNumbered(single_breed)
        for idv in pedigree_all:
            pedigree_all[idv][f_breed] = single_breed.get(
                idv, dict()).get('id_num', 0)
        # write pedigree file of sinale breed
        output_file_list_breed.append(str(len(single_breed)))
        output_file_list_breed.append(
            str(_WritePedigree(single_breed, id_list, f_breed, tmp_prefix)))
        gene_id_breed = [x for x in gene_id_breed if x[0] in single_breed]
        output_file_list_breed.append(str(len(gene_id_breed)))
        for idv in gene_id_breed:
            idv.append(str(single_breed.get(idv[0]).get('id_num')))
            idv_breed = single_breed.get(idv[0]).get('breed')
            if idv_breed == f_breed:
                idv.append("1")
            else:
                if single_breed.get(idv[0]).get('sire') in single_breed:
                    idv.append("2")  # sire is purebred
                elif single_breed.get(idv[0]).get('dam') in single_breed:
                    idv.append("3")  # dam is purebred
        output_file_gene = "{0}_{1}_gene_id".format(tmp_prefix, f_breed)
        f_gene = open(output_file_gene, "w+")
        # this file like id, sort in gene file, sort in pedigree, parent which is need breed(father is 2, mother 3 and 1 is purebred)
        f_gene.writelines([" ".join(x) + "\n" for x in gene_id_breed])
        f_gene.close()
        # output_file_gene = "{0}_{1}_gene_crossbred_id".format(tmp_prefix, f_breed)
        # f_gene = open(output_file_gene, "w+")
        # # this file like id, sort in gene file, sort in pedigree, parent which is need breed(father is 2, mother 3 and 1 is purebred)
        # f_gene.writelines( [ " ".join(x) + "\n" for x in gene_id_breed if x[3] != '1'] )
        # f_gene.close()
        output_file_list_breed.append(output_file_gene)
        output_file_list.append(" ".join(output_file_list_breed))
        print("Finish analyzing pedigree of breed {0}.\n".format(f_breed))
        # TODO create two files for purebred individual id and crossbred individual id
        # there ia a question: how to deal with the individual which have more than 2 breed like D-L-W?
        # maybe i can find the answer in the paper which study on triangle pig
    pedigree_all, id_list_all = _ReNumbered(pedigree_all)
    output_file_list.append(" ".join([str(len(pedigree_all)), str(_WritePedigreeAll(
        pedigree_all, id_list_all, breed_list, tmp_prefix))]))
    print("Finish analyzing pedigree.\n")
    # print("\t".join(output_file_list))
    return "\t".join(output_file_list)


def _ReadPedigree(filename_pedigree, header):
    # Read pedigree files
    pedigree = dict()
    breed = set()
    error_line = list()
    # Read pedigree files
    with open(filename_pedigree) as f:
        for line in f:
            if line == '\n':
                continue
            line = line.rstrip('\n').split(' ')
            # Record rows with the wrong number
            if len(line) != 5:
                error_line.append(line)
            # Generation (sort item) converted to number
            # TODO import generation, maybe birthdays
            line[3] = int(line[3])
            # Store as a nested dictionary
            pedigree[line[0]] = dict(zip(header, line))
            # Record breed information
            breed.add(line[4])
    return [pedigree, breed, error_line]


def _AddIdv(pedigree, header):
    # Complement the pedigree, any individual has one item
    add_idv = dict()
    for idv in pedigree:
        if pedigree.get(idv).get('breed') == '0':
            continue
        f_sire = pedigree.get(idv).get('sire')
        if (f_sire not in pedigree) and (f_sire != '0'):
            add_idv[f_sire] = dict(
                zip(header, [f_sire, '0', '0', 0, pedigree.get(idv).get('breed')]))
        f_dam = pedigree.get(idv).get('dam')
        if (f_dam not in pedigree) and (f_dam != '0'):
            add_idv[f_dam] = dict(
                zip(header, [f_dam, '0', '0', 0, pedigree.get(idv).get('breed')]))
    pedigree.update(add_idv)
    for idv in pedigree:
        if pedigree.get(idv).get('breed') == '0':
            if pedigree.get(idv).get('sire') not in pedigree:
                pedigree.get(idv)['sire'] = '0'
            if pedigree.get(idv).get('dam') not in pedigree:
                pedigree.get(idv)['dam'] = '0'
    return pedigree


def _CalculationGeneration(pedigree, idv):
    # Iterative solution generation
    # Result like:
    # {'1': {'id': '1', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'A'},
    #  '2': {'id': '2', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'A'},
    #  '3': {'id': '3', 'sire': '1', 'dam': '2', 'generations': 2, 'breed': 'A'},
    #  '4': {'id': '4', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'B'},
    #  '5': {'id': '5', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'B'},
    #  '6': {'id': '6', 'sire': '4', 'dam': '5', 'generations': 2, 'breed': 'B'},
    #  '7': {'id': '7', 'sire': '2', 'dam': '6', 'generations': 3, 'breed': '0'},
    #  '8': {'id': '8', 'sire': '3', 'dam': '6', 'generations': 3, 'breed': '0'}}
    # TODO need logic for some generations had been imported
    sire = pedigree.get(idv, {}).get('sire', '0')
    dam = pedigree.get(idv, {}).get('dam', '0')
    id_generation = pedigree.get(idv, {}).get('generations', 0)
    sire_generation = pedigree.get(sire, {}).get('generations', 0)
    dam_generation = pedigree.get(dam,  {}).get('generations', 0)
    if id_generation:
        if (id_generation > sire_generation) and (id_generation > dam_generation):
            return pedigree
    if sire != '0' and dam != '0':
        if sire_generation:
            if dam_generation:
                pass
            else:
                pedigree = _CalculationGeneration(pedigree, dam)
                dam_generation = pedigree.get(dam,  {}).get('generations', 0)
        else:
            if dam_generation:
                pedigree = _CalculationGeneration(pedigree, sire)
                sire_generation = pedigree.get(sire,  {}).get('generations', 0)
            else:
                pedigree = _CalculationGeneration(pedigree, sire)
                sire_generation = pedigree.get(sire,  {}).get('generations', 0)
                pedigree = _CalculationGeneration(pedigree, dam)
                dam_generation = pedigree.get(dam,  {}).get('generations', 0)
        pedigree.get(idv)['generations'] = max(
            sire_generation, dam_generation) + 1
    elif sire != '0' and dam == '0':
        if not sire_generation:
            pedigree = _CalculationGeneration(pedigree, sire)
            sire_generation = pedigree.get(sire,  {}).get('generations', 0)
        pedigree.get(idv)['generations'] = sire_generation + 1
    elif sire == '0' and dam != '0':
        if not dam_generation:
            pedigree = _CalculationGeneration(pedigree, dam)
            dam_generation = pedigree.get(dam,  {}).get('generations', 0)
        pedigree.get(idv)['generations'] = dam_generation + 1
    elif sire == '0' and dam == '0':
        pedigree.get(idv)['generations'] = 1
    return pedigree


def _SplitPedigree(pedigree, breed):
    # calculate lineage
    # Result like breed:
    # {'A': {'1': {'id': '1', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'A', 'lineage': 1},
    #       '2': {'id': '2', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'A', 'lineage': 1},
    #       '3': {'id': '3', 'sire': '1', 'dam': '2', 'generations': 2, 'breed': 'A', 'lineage': 1},
    #       '7': {'id': '7', 'sire': '2', 'dam': '6', 'generations': 3, 'breed': '0', 'lineage': 0.5},
    #       '8': {'id': '8', 'sire': '3', 'dam': '6', 'generations': 3, 'breed': '0', 'lineage': 0.5}},
    # 'B': {'4': {'id': '4', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'B', 'lineage': 1},
    #       '5': {'id': '5', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'B', 'lineage': 1},
    #       '6': {'id': '6', 'sire': '4', 'dam': '5', 'generations': 2, 'breed': 'B', 'lineage': 1},
    #       '7': {'id': '7', 'sire': '2', 'dam': '6', 'generations': 3, 'breed': '0', 'lineage': 0.5},
    #       '8': {'id': '8', 'sire': '3', 'dam': '6', 'generations': 3, 'breed': '0', 'lineage': 0.5}}}
    import copy
    for idv in pedigree:
        f_breed = pedigree.get(idv).get('breed')
        breed.get(f_breed)[idv] = copy.deepcopy(pedigree.get(idv))
        if f_breed != '0':
            breed.get(f_breed).get(idv)['lineage'] = 1
    if '0' not in breed:
        return breed
    crossbred = breed.pop('0')

    def CalculationLineage(single_breed, crossbred, idv):
        if idv in single_breed:
            return single_breed
        sire = crossbred.get(idv).get('sire')
        dam = crossbred.get(idv).get('dam')
        if sire in crossbred:
            single_breed = CalculationLineage(single_breed, crossbred, sire)
        if dam in crossbred:
            single_breed = CalculationLineage(single_breed, crossbred, dam)
        sire_lineage = single_breed.get(sire, {}).get('lineage', 0)
        dam_lineage = single_breed.get(dam,  {}).get('lineage', 0)
        id_lineage = (sire_lineage + dam_lineage) / 2.0
        if id_lineage:
            single_breed[idv] = copy.deepcopy(crossbred.get(idv))
            single_breed.get(idv)['lineage'] = id_lineage
        return single_breed
    for traverse_breed in breed:
        for idv in crossbred:
            breed[traverse_breed] = CalculationLineage(
                breed.get(traverse_breed), crossbred, idv)
    return breed


def _ReNumbered(single_breed):
    # Recode the genealogy and provide it to C
    id_list = []
    for idv in single_breed:
        id_list.append([idv, single_breed.get(idv).get('generations')])
    id_list.sort(key=lambda x: x[1], reverse=False)
    id_list = [lst[0] for lst in id_list]
    id_sort = list(range(1, len(id_list) + 1))
    id_hash = dict(zip(id_list, id_sort))
    id_list = list(zip(id_list, id_sort))
    # {'1': {'id': '1', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'A', 'lineage': 1,
    #        'id_num': 1, 'sire_num': 0, 'dam_num': 0},
    #  '2': {'id': '2', 'sire': '0', 'dam': '0', 'generations': 1, 'breed': 'A', 'lineage': 1,
    #        'id_num': 2, 'sire_num': 0, 'dam_num': 0},
    #  '3': {'id': '3', 'sire': '1', 'dam': '2', 'generations': 2, 'breed': 'A', 'lineage': 1,
    #        'id_num': 3, 'sire_num': 1, 'dam_num': 2},
    #  '7': {'id': '7', 'sire': '2', 'dam': '6', 'generations': 3, 'breed': '0', 'lineage': 0.5,
    #        'id_num': 4, 'sire_num': 2, 'dam_num': 0},
    #  '8': {'id': '8', 'sire': '3', 'dam': '6', 'generations': 3, 'breed': '0', 'lineage': 0.5,
    #        'id_num': 5, 'sire_num': 3, 'dam_num': 0}}
    for idv in single_breed:
        single_breed.get(idv)['id_num'] = id_hash.get(idv)
        single_breed.get(idv)['sire_num'] = id_hash.get(
            single_breed.get(idv).get('sire'), 0)
        single_breed.get(idv)['dam_num'] = id_hash.get(
            single_breed.get(idv).get('dam'), 0)
    return [single_breed, id_list]


def _WritePedigree(single_breed, id_list, f_breed, tmp_prefix):
    # Write files by breeds
    output_file = "{0}_{1}_pedigree".format(tmp_prefix, f_breed)
    f = open(output_file, "w+")
    for id in [lst[0] for lst in id_list]:
        lines = single_breed.get(id)
        lines = [lines.get('id'), str(lines.get('id_num')), lines.get('sire'), str(lines.get('sire_num')),
                 lines.get('dam'), str(lines.get('dam_num')), str(
                     lines.get('generations')),
                 lines.get('breed'), str(lines.get('lineage'))]
        lines = ' '.join(lines) + '\n'
        f.write(lines)
    f.close()
    return output_file


def _WritePedigreeAll(pedigree_all, id_list_all, breed_list, tmp_prefix):
    # Write files by breeds
    if len(breed_list) < 2:
        breed_list.append('')
    output_file = "{0}_pedigree_all".format(tmp_prefix)
    f = open(output_file, "w+")
    for id in [lst[0] for lst in id_list_all]:
        lines = pedigree_all.get(id)
        lines = [lines.get('id'), str(lines.get('id_num')), lines.get('sire'), str(lines.get('sire_num')),
                 lines.get('dam'), str(lines.get('dam_num')), str(
            lines.get('generations')),
            lines.get('breed'), str(lines.get(breed_list[0])), str(lines.get(breed_list[1], ''))]
        lines = [x for x in lines if x != '']
        lines = ' '.join(lines) + '\n'
        f.write(lines)
    f.close()
    return output_file
