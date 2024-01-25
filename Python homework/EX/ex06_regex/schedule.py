"""Create schedule from the given file."""
import re


pattern = r'(?<=\s|\n)(\d{1,2})[^\d](\d{1,2})\s+([a-zA-Z]+)'


def create_dictionary_from_pattern(pattern: str, input_string: str) -> dict:
    """Create dictionary from pattern and normalize it."""
    schedule_dict = {}
    for match in re.finditer(pattern, input_string):
        if int(match.group(2)) > 60:
            continue
        if int(match.group(1)) > 24:
            continue
        else:
            schedule_dict.setdefault(normalize(match.group(1), match.group(2)), []).append(match.group(3).lower())
    return schedule_dict


def normalize(hours: str, minutes: str) -> str:
    """Add missing 0's to the minutes and remove extra 0's from hours."""
    time = ""
    if len(hours) == 2:
        time += hours + ":"
    if len(hours) == 1:
        time += "0" + hours + ":"
    if len(minutes) == 1:
        time += "0" + minutes
    if len(minutes) == 2:
        time += minutes
    return time


def sort_dictionary(pattern_dictionary: dict) -> dict:
    """Sort dictionary by time."""
    sorted_items = dict(sorted(pattern_dictionary.items(), key=lambda x: x[0]))
    return sorted_items


def get_formatted_time(time: str) -> str:
    """Format 24 hour time to the 12 hour time."""
    input_time = time.replace(":", "")
    formatted_time = ""
    if 12 < int(input_time[0:2]) < 24:
        formatted_time += f"{int(input_time[:2]) - 12}:{input_time[2:4]} PM"
    else:
        if int(input_time[0:2]) == 0:
            formatted_time += f"12:{input_time[2:4]} AM"
        if int(input_time[0:2]) == 12:
            formatted_time += f"12:{input_time[2:4]} PM"
        if 0 < int(input_time[0:2]) < 12:
            formatted_time += f"{int(input_time[:2])}:{input_time[2:4]} AM"
    return formatted_time


def get_table_sizes(schedule_dict_elements: dict) -> list:
    """Get the maximum sizes for table."""
    max_sizes_list = []
    max_time = 0
    max_entries_size = 0
    if schedule_dict_elements:
        for time, entries in schedule_dict_elements.items():
            times = [00, 0, 10, 11, 12, 22, 23]
            if int(time[3:5]) < 60 and int(time[:2]) in times:
                max_time = 10
            if int(time[3:5]) < 60 and int(time[:2]) not in times and max_time != 10:
                max_time = 9
            entries_count = 0
            entries_list = []
            if int(time[3:5]) < 60 and int(time[:2]) < 24:
                for entry in entries:
                    if entry not in entries_list:
                        entries_list.append(entry)
                        entries_count += len(entry) + 2
            if max_entries_size < entries_count:
                max_entries_size = entries_count
        max_sizes_list.append(max_time)
        if max_entries_size >= 9:
            max_sizes_list.append(max_entries_size)
        else:
            max_sizes_list.append(9)
        return max_sizes_list
    else:
        return []


def no_entries_found() -> list:
    """Create table when no entries found."""
    table = []
    main_line = '-' * 20
    table.append(main_line)
    table.append(f"{'|' : <0}{'time' : >{6}} |"
                 f" entries{'|' : >{3}}")
    table.append(main_line)
    table.append(f"{'|' : <0} No entries found{'|' : >{2}}")
    table.append(main_line)
    return table


def create_heading_to_table(time_column_width, entries_column_width) -> list:
    """Create heading part for the table."""
    table = []
    main_line = '-' * (time_column_width + entries_column_width + 3)
    heading_line = ""
    if time_column_width == 10:
        heading_line = f"|{'time' : >{time_column_width - 1}} | entries{'|' : >{(entries_column_width) - 7}}"
    if time_column_width == 9:
        heading_line = f"|{'time' : >{(time_column_width - 1)}} | entries{'|' : >{(entries_column_width) - 7}}"
    table.append(main_line)
    table.append(heading_line)
    table.append(main_line)
    return table


def add_data_to_table(table: list, time_column_width: int, entries_column_width: int, key: str, element_values: str) -> None:
    """Add time and entries to the table."""
    if int(key[3:5]) < 60 and int(key[0:2]) < 24:
        if time_column_width == 10:
            if len(get_formatted_time(key)) == 8:
                table.append(f"| {get_formatted_time(key) : >{1}} | "
                             f"{element_values}{'|' : >{entries_column_width - len(element_values)}}")
            if len(get_formatted_time(key)) == 7:
                table.append(f"|  {get_formatted_time(key) : >{1}} | "
                             f"{element_values}{'|' : >{entries_column_width - len(element_values)}}")
        if time_column_width == 9:
            table.append(f"| {get_formatted_time(key) : >{1}} | "
                         f"{element_values}{'|' : >{entries_column_width - len(element_values)}}")


def create_table(input_string: str) -> list:
    """Create table."""
    input_dict = create_dictionary_from_pattern(pattern, input_string)
    if input_string and input_dict:
        table_sizes = get_table_sizes(input_dict)
        time_column_width = table_sizes[0]
        entries_column_width = table_sizes[1]
        table = create_heading_to_table(time_column_width, entries_column_width)
        for key, values in sort_dictionary(input_dict).items():
            element_values_list = []
            element_values = ""
            for value in values:
                if value not in element_values_list:
                    element_values_list.append(value)
            element_values += ", ".join(element_values_list)
            if int(key[3:5]) >= 60:
                continue
            if int(key[0:2]) >= 24:
                continue
            add_data_to_table(table, time_column_width, entries_column_width, key, element_values)
        if len(table) > 3:
            table.append('-' * (time_column_width + entries_column_width + 3))
            return table
        else:
            return no_entries_found()
    else:
        return no_entries_found()


def create_schedule_string(input_string: str) -> str:
    """Create schedule string from the given input string."""
    return "\n".join(create_table(input_string))


def create_schedule_file(input_filename: str, output_filename: str) -> None:
    """Create schedule file from the given input file."""
    f = open(input_filename, "r")
    schedule = create_schedule_string(f.read())
    g = open(output_filename, "w")
    g.write(schedule)
