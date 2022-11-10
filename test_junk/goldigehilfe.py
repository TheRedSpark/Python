


def main():
    point1 = [6,2]
    point2 = [7,5]
    m = (point2[1]-point1[1])/(point2[0]-point1[0])
    return m

if __name__ == "__main__":
    anstieg = main()
    print(f"Der Anstieg ist {anstieg}")