from data_loader import load_personas

df = load_personas()
print(f'Total personas: {len(df)}')
print(f'Unique names: {df["name"].nunique()}')
print(f'Duplicates: {len(df) - df["name"].nunique()}')

# Show duplicate names
duplicates = df[df.duplicated(subset=['name'], keep=False)].sort_values('name')
if len(duplicates) > 0:
    print(f'\nDuplicate names found:')
    print(duplicates[['name', 'age', 'city_tier']].head(20))
