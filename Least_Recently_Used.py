pages = list(map(int, input("Enter page reference string: ").split()))
capacity = int(input("Enter number of frames: "))

frames = []
page_faults = 0

for page in pages:

    if page not in frames:

        page_faults += 1

        if len(frames) < capacity:
            frames.append(page)
        else:
            frames.pop(0)
            frames.append(page)

    else:
        frames.remove(page)
        frames.append(page)

    print("Page:", page, "Frames:", frames)

print("\nTotal Page Faults =", page_faults)