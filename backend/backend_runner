import subprocess

print("\n Step 1: generate rider data (rider_generator.py)")
subprocess.run(["python", "rider_generator.py"], check=True)

print("\n Step 2: generate trail map + stimulate rider routes + track diagram (rider_stimulations.py)")
subprocess.run(["python", "rider_stimulations.py"], check=True)

print("Complete the complete backend process！")
print("\n Riders_simulation.csv、rider_paths_plot_colored.png、rider_path_errors.csv generated at /mnt/data/")
