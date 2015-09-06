from card import deal, format_input


def get_test_data(num_training, num_validation, num_test):
    samples = {"training": [], "validation": [], "test": []}
    for i in range(num_training):
        samples["training"].append(make_sample(*deal(2)))
    for i in range(num_validation):
        samples["validation"].append(make_sample(*deal(2)))
    for i in range(num_test):
        samples["test"].append(make_sample(*deal(2)))


def make_sample(card, prev_card):
    is_correct = card[0] == prev_card[0] or card[1] == prev_card[1]
    return [format_input(card, prev_card), [is_correct]]
