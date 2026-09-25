
def distance_converter():
    print("\n--- Distance ---")
    print("1. Kilometers → Miles")
    print("2. Miles → Kilometers")

    choice = input("Choose conversion: ")

    if choice == "1":
        try:
            value = float(input("Enter kilometers: "))
            converted = value * 0.621371

            print(f"\n{value} km → {converted:.2f} miles")
        except ValueError:
            print("Invalid value. Please enter a number.")

    elif choice == "2":
        try:
            value = float(input("Enter miles: "))
            converted = value * 1.60934

            print(f"\n{value} miles → {converted:.2f} km")
        except ValueError:
            print("Invalid value. Please enter a number.")

    else:
        print("Invalid conversion choice.")


def temperature_converter():
    print("\n--- Temperature ---")
    print("1. Celsius → Fahrenheit")
    print("2. Fahrenheit → Celsius")

    choice = input("Choose conversion: ")

    if choice == "1":
        try:
            value = float(input("Enter Celsius: "))
            converted = (value * 9 / 5) + 32

            print(f"\n{value} °C → {converted:.2f} °F")
        except ValueError:
            print("Invalid value. Please enter a number.")

    elif choice == "2":
        try:
            value = float(input("Enter Fahrenheit: "))
            converted = (value - 32) * 5 / 9

            print(f"\n{value} °F → {converted:.2f} °C")
        except ValueError:
            print("Invalid value. Please enter a number.")

    else:
        print("Invalid conversion choice.")


def weight_converter():
    print("\n--- Weight ---")
    print("1. Kilograms → Pounds")
    print("2. Pounds → Kilograms")

    choice = input("Choose conversion: ")

    if choice == "1":
        try:
            value = float(input("Enter kilograms: "))
            converted = value * 2.20462

            print(f"\n{value} kg → {converted:.2f} lb")
        except ValueError:
            print("Invalid value. Please enter a number.")

    elif choice == "2":
        try:
            value = float(input("Enter pounds: "))
            converted = value * 0.453592

            print(f"\n{value} lb → {converted:.2f} kg")
        except ValueError:
            print("Invalid value. Please enter a number.")

    else:
        print("Invalid conversion choice.")


def main():
    while True:
        print("\n===== Measurement Converter =====")
        print("1. Distance")
        print("2. Temperature")
        print("3. Weight")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            distance_converter()

        elif choice == "2":
            temperature_converter()

        elif choice == "3":
            weight_converter()

        elif choice == "4":
            print("Thanks for using Measurement Converter. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-4.")


# if __name__ == "__main__":

main()