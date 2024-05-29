from data_preparation import DELIMETER


@DeprecationWarning
def _calculate_iou_local(pred_start, pred_end, true_start, true_end):
    pred_seq = list(range(pred_start, pred_end))
    true_seq = list(range(true_start, true_end))
    
    intersection_area = len(set(pred_seq).intersection(set(true_seq)))
    union_area = len(set(pred_seq).union(set(true_seq)))
    
    return intersection_area / union_area

def calculate_iou(pred_starts, pred_ends, true_starts, true_ends):
    pred_seq = sum([list(range(pred_start, pred_end)) for pred_start, pred_end in zip(pred_starts, pred_ends)], start=[])
    true_seq = sum([list(range(true_start, true_end)) for true_start, true_end in zip(true_starts, true_ends)], start=[])
    
    intersection_area = len(set(pred_seq).intersection(set(true_seq)))
    union_area = len(set(pred_seq).union(set(true_seq)))
    
    return intersection_area / union_area


def cook_start_end(str_start_end: str) -> list[int, int]:
    start, end = str_start_end.split(',')
    int_start = int(start[1:])
    int_end = int(end[:len(end) - 1])
    return int_start, int_end


def main():
    ious = []
    with open('processed_data/llama_symptoms_start_end.txt', 'r') as file_start_end:
        yagpt_start_end = file_start_end.readlines()
    with open('processed_data/sorted_symptoms_start_end.txt', 'r') as file_start_end:
        right_start_end = file_start_end.readlines()
    for yagpt, right in zip(yagpt_start_end, right_start_end):
        iou = 0
        yagpt = [x.strip() for x in yagpt.split(DELIMETER) if x.strip() != '']
        right = [x.strip() for x in right.split(DELIMETER) if x.strip() != '']
        if (right == []) and (yagpt == []):
            iou = 1
        elif (right == []) or (yagpt == []):
            iou = 0
        else:
            yagpt_starts = [cook_start_end(x)[0] for x in yagpt]
            yagpt_ends = [cook_start_end(x)[1] for x in yagpt]
            right_starts = [cook_start_end(x)[0] for x in right]
            right_ends = [cook_start_end(x)[1] for x in right]
            iou = calculate_iou(yagpt_starts, yagpt_ends, right_starts, right_ends)
        ious.append(iou)
        print(yagpt, right)
        print(iou)
    print(f'Mean IoU: {sum(ious) / len(ious)}')



if __name__ == '__main__':
    main()
