from colorama import init, Fore, Style

# Initialize colorama for colored output (works in console and PyInstaller .exe)
init()


def get_people_names():
    while True:
        try:
            names_input = input(
                f"Enter {Fore.RED}names{Style.RESET_ALL} separated by commas (e.g., {Fore.RED}Fross, Twixx, Raff{Style.RESET_ALL}): ").strip()
            names = [name.strip() for name in names_input.split(',') if name.strip()]
            if not names:
                print(f"{Fore.RED}At least one valid name must be entered!{Style.RESET_ALL}")
                continue
            return names
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program interrupted by user. Exiting...{Style.RESET_ALL}")
            exit(0)


def get_box_counts():
    box_sizes = [32, 24, 16, 8, 4]
    box_counts = {}
    for size in box_sizes:
        while True:
            try:
                count = int(input(f"Enter number of {Fore.BLUE}size {size}{Style.RESET_ALL} boxes: "))
                if count >= 0:
                    box_counts[size] = count
                    break
                print(f"{Fore.RED}Please enter a non-negative number!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program interrupted by user. Exiting...{Style.RESET_ALL}")
                exit(0)
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
    print(f"\n{Fore.RED}Distribution Results:{Style.RESET_ALL}")
    for name in names:
        print(f"\n{Fore.RED}{name}{Style.RESET_ALL}:")
        total_units = 0
        for size, count in distributions[name].items():
            if count > 0:
                print(f"  {Fore.GREEN}{count}{Style.RESET_ALL} box(es) of {Fore.BLUE}size {size}{Style.RESET_ALL}")
                total_units += count * size
        if name == names[0]:
            total_units += remainder
            if remainder > 0:
                print(f"  + {Fore.GREEN}{remainder}{Style.RESET_ALL} extra units (as OP leader)")
        print(f"  Total units: {Fore.GREEN}{total_units}{Style.RESET_ALL}")


def main():
    while True:
        print(f"{Fore.RED}Box Splitter Program{Style.RESET_ALL}")
        print("-" * 20)

        # Get people names
        names = get_people_names()

        # Get box counts
        box_counts = get_box_counts()

        # Calculate and distribute
        distributions, base_units_per_person, remainder = distribute_boxes(names, box_counts)

        # Print results
        print(f"\nTotal units: {Fore.GREEN}{calculate_total_units(box_counts)}{Style.RESET_ALL}")
        print(f"Base units per person: {Fore.GREEN}{base_units_per_person}{Style.RESET_ALL}")
        if remainder > 0:
            print(
                f"Remaining units to OP leader ({Fore.RED}{names[0]}{Style.RESET_ALL}): {Fore.GREEN}{remainder}{Style.RESET_ALL}")
        print_distribution(names, distributions, base_units_per_person, remainder)

        # Prompt to reset or exit
        while True:
            try:
                choice = input(
                    f"\nWould you like to reset and start again? ({Fore.GREEN}yes{Style.RESET_ALL}/{Fore.GREEN}no{Style.RESET_ALL}): ").strip().lower()
                if choice in ['yes', 'y']:
                    print(f"\n{Fore.RED}Restarting program...{Style.RESET_ALL}\n")
                    break
                elif choice in ['no', 'n']:
                    print(f"\n{Fore.RED}Exiting program...{Style.RESET_ALL}")
                    return
                else:
                    print(f"{Fore.RED}Please enter 'yes' or 'no'.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program interrupted by user. Exiting...{Style.RESET_ALL}")
                return


if __name__ == "__main__":
    main()