import matplotlib.pyplot as plt
from utils import load_game_data
from models import ResourceOptimizer

def analyze_upgrade_paths():
    data = load_game_data()
    if data is None:
        print("Failed to load data. Exiting...")
        return
    buildings, upgrades, production = data
    optimizer = ResourceOptimizer(buildings, upgrades, production)
    available_resources = {
        'gold': 10000000,
        'elixir': 10000000,
        'dark_elixir': 200000
    }
    
    upgrade_path = optimizer.optimize_upgrade_path(available_resources)
    if not upgrade_path:
        print("No viable upgrades found!")
        return

    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    fig = plt.figure(figsize=(15, 10))
    
    ax1 = plt.subplot(2, 2, 1)
    categories = ['Resource', 'Storage', 'Defense']
    colors = ['#2ecc71', '#3498db', '#e74c3c'] 
    y_position = 0
    yticks = []
    ylabels = []
    
    for category, color in zip(categories, colors):
        category_upgrades = [u for u in upgrade_path if u['category'].lower() == category.lower()]
        if category_upgrades:
            rois = [u['roi'] for u in category_upgrades]
            names = [f"{u['building']} L{u['level']}" for u in category_upgrades] 
            positions = range(y_position, y_position + len(category_upgrades))
            ax1.barh(positions, rois, color=color, alpha=0.7, label=category)
            yticks.extend(positions)
            ylabels.extend(names)
            y_position += len(category_upgrades)
    
    ax1.set_yticks(yticks)
    ax1.set_yticklabels(ylabels)
    ax1.set_title('ROI by Building Category')
    ax1.set_xlabel('ROI (%)')
    ax1.legend()    
    plt.tight_layout()

    fig2 = plt.figure(figsize=(12, 8))
    ax2 = fig2.add_subplot(111)
    total_time = optimizer.calculate_build_time(upgrade_path)
    build_times = [u['time_hours'] for u in upgrade_path[:10]]
    buildings = [f"{u['building']} L{u['level']}" for u in upgrade_path[:10]]
    ax2.barh(range(len(buildings)), build_times, color='#9b59b6')
    ax2.set_yticks(range(len(buildings)))
    ax2.set_yticklabels(buildings)
    ax2.set_title(f'Top 10 Upgrade Times (Total: {total_time/24:.1f} days)')
    ax2.set_xlabel('Hours')    
    plt.tight_layout()

    fig3 = plt.figure(figsize=(10, 10))
    ax3 = fig3.add_subplot(111)
    resources = ['gold', 'elixir', 'dark_elixir']
    resource_costs = {r: sum(u['cost'] for u in upgrade_path 
                           if u['resource_type'] == r)
                     for r in resources}
    
    plt.pie(resource_costs.values(),
            labels=[r.replace('_', ' ').title() for r in resources],
            autopct='%1.1f%%',
            colors=['#f1c40f', '#e74c3c', '#8e44ad'])
    ax3.set_title('Resource Distribution')
    
    plt.tight_layout()
    
    # 4. Builder Utilization
    fig4 = plt.figure(figsize=(10, 8))
    ax4 = fig4.add_subplot(111)
    builder_times = [0] * optimizer.builders
    for time in sorted([u['time_hours'] for u in upgrade_path], reverse=True):
        min_builder = builder_times.index(min(builder_times))
        builder_times[min_builder] += time
    
    ax4.bar(range(1, optimizer.builders + 1), 
            [t/24 for t in builder_times],
            color='#2980b9')
    ax4.set_title('Builder Utilization')
    ax4.set_xlabel('Builder Number')
    ax4.set_ylabel('Days of Work')
    plt.tight_layout()
    plt.show()
    print("\nUpgrade Path Analysis:")
    print(f"Total Upgrades: {len(upgrade_path)}")
    print(f"Total Build Time: {total_time/24:.1f} days (with {optimizer.builders} builders)")
    print("\nResource Requirements:")
    for res, cost in resource_costs.items():
        print(f"{res.replace('_', ' ').title()}: {cost:,}")
    print("\nTop 10 Recommended Upgrades:")
    for i, upgrade in enumerate(upgrade_path[:10], 1):
        print(f"\n{i}. {upgrade['building']} to level {upgrade['level']}")
        print(f"   Category: {upgrade['category']}")
        print(f"   ROI: {upgrade['roi']:.1f}%")
        print(f"   Cost: {upgrade['cost']:,} {upgrade['resource_type']}")
        print(f"   Build Time: {upgrade['time_hours']:.1f} hours")

def main():
    analyze_upgrade_paths()

if __name__ == "__main__":
    main()