from data_generator import DataGenerator

if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate_scripts()
    print(f"Total unique Sonic Pi scripts generated: {generator.total_scripts}")
