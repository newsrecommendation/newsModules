# 参数说明
# 1、triple2id.txt
# 存放的是head_index, tail_index, relation_index
# head_index，tail_index分别表示该实体（head/tail）在各三元组实体中的位置
# relation_list表示关系在三元组关系中出现的位置
# 2、entit2id.txt存的是实体（head,tail）在所有三元组(kg.txt中的)中出现的位置（entity在Kg中的编号,entity在kg里所有实体的位置）
# 3、relation2id.txt存的是关系在所有三元组中存在的位置
# 对于关系或实体，只要值相同就是同一关系/实体
def prepare_data(kg_in, triple_out, relation_out, entity_out):
    relation2index = {}
    entity2index = {}
    relation_list = []
    entity_list = []

    reader_kg = open(kg_in, encoding='utf-8')
    writer_triple = open(triple_out, 'w', encoding='utf-8')
    writer_relation = open(relation_out, 'w', encoding='utf-8')
    writer_entity = open(entity_out, 'w', encoding='utf-8')

    entity_cnt = 0
    relation_cnt = 0
    triple_cnt = 0

    print('reading knowledge graph ...')
    kg = reader_kg.read().strip().split('\n')

    print('writing triples to triple2id.txt ...')
    writer_triple.write('%d\n' % len(kg))
    for line in kg:
        array = line.split('\t')
        head = array[0]
        relation = array[1]
        tail = array[2]
        if head in entity2index:
            head_index = entity2index[head]
        else:
            head_index = entity_cnt
            entity2index[head] = entity_cnt
            entity_list.append(head)
            entity_cnt += 1
        if tail in entity2index:
            tail_index = entity2index[tail]
        else:
            tail_index = entity_cnt
            entity2index[tail] = entity_cnt
            entity_list.append(tail)
            entity_cnt += 1
        if relation in relation2index:
            relation_index = relation2index[relation]
        else:
            relation_index = relation_cnt
            relation2index[relation] = relation_cnt
            relation_list.append(relation)
            relation_cnt += 1
        writer_triple.write(
            '%d\t%d\t%d\n' % (head_index, tail_index, relation_index))
        triple_cnt += 1
    print('triple size: %d' % triple_cnt)

    print('writing entities to entity2id.txt ...')
    writer_entity.write('%d\n' % entity_cnt)
    for i, entity in enumerate(entity_list):
        writer_entity.write('%s\t%d\n' % (entity, i))
    print('entity size: %d' % entity_cnt)

    print('writing relations to relation2id.txt ...')
    writer_relation.write('%d\n' % relation_cnt)
    for i, relation in enumerate(relation_list):
        writer_relation.write('%s\t%d\n' % (relation, i))
    print('relation size: %d' % relation_cnt)

    reader_kg.close()


if __name__ == '__main__':
    prefix = './'
    kg_in = prefix + 'jgw_classtriples.txt'
    triple_out = prefix + 'jgw_triple2id.txt'
    relation_out = prefix + 'jgw_relation2id.txt'
    entity_out = prefix + 'jgw_entity2id.txt'
    prepare_data(kg_in=kg_in, triple_out=triple_out, relation_out=relation_out, entity_out=entity_out)
    # prepare_data(kg_in='kg.txt', triple_out='triple2id.txt', relation_out='relation2id.txt', entity_out='entity2id.txt')
