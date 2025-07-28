def get_people_names():
    while True:
        names_input = input("Enter names separated by commas (e.g., Fross, Twixx, Raff): ").strip()
        names = [name.strip() for name in names_input.split(',') if name.strip()]
        if not names:
            print("At least one valid name must be entered!")
            continue
        return names

def get_box_counts():
    box_sizes = [32, 24, 16, 8, 4]
    box_counts = {}
    for size in box_sizes:
        while True:
            try:
                count = int(input(f"Enter number of boxes of size {size}: "))
                if count >= 0:
                    box_counts[size] = count
                    break
                print("Please enter a non-negative number!")
            except ValueError:
                print("Please enter a valid number!")
    return box_counts


def calculate_total_units(box_counts):
    return sum(size * count for size, count in box_counts.items())


def distribute_boxes(names, box_counts):
    total_units = calculate_total_units(box_counts)
    num_people = len(names)
    base_units_per_person = total_units // num_people
    remainder = total_units % num_people

    distributions = {name: {32: 0, 24: 0, 16: 0, 8: 0, 4: 0} for name in names}
    remaining_counts = box_counts.copy()

    # Distribute to each person except the OP leader
    for name in names[1:]:
        units_needed = base_units_per_person
        for size in sorted(remaining_counts.keys(), reverse=True):
            while units_needed >= size and remaining_counts[size] > 0:
                num_boxes = min(units_needed // size, remaining_counts[size])
                distributions[name][size] = num_boxes
                units_needed -= num_boxes * size
                remaining_counts[size] -= num_boxes

    # OP leader gets remaining boxes
    for size in sorted(remaining_counts.keys(), reverse=True):
        distributions[names[0]][size] = remaining_counts[size]

    return distributions, base_units_per_person, remainder


def print_distribution(names, distributions, base_units_per_person, remainder):
    print("\nDistribution Results:")
    for name in names:
        print(f"\n{name}:")
        total_units = 0
        for size, count in distributions[name].items():
            if count > 0:
                print(f"  {count} box(es) of size {size}")
                total_units += count * size
        if name == names[0]:
            total_units += remainder
            if remainder > 0:
                print(f"  + {remainder} extra units (as OP leader)")
        print(f"  Total units: {total_units}")


def main():
    print("Box Splitter Program")
    print("-" * 20)

    # Get people names
    names = get_people_names()

    # Get box counts
    box_counts = get_box_counts()

    # Calculate and distribute
    distributions, base_units_per_person, remainder = distribute_boxes(names, box_counts)

    # Print results
    print(f"\nTotal units: {calculate_total_units(box_counts)}")
    print(f"Base units per person: {base_units_per_person}")
    if remainder > 0:
        print(f"Remaining units to OP leader ({names[0]}): {remainder}")
    print_distribution(names, distributions, base_units_per_person, remainder)


if __name__ == "__main__":
    main()