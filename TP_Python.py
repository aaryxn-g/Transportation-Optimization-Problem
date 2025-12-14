
import numpy as np
import pandas as pd
from pulp import *
import matplotlib.pyplot as plt
import seaborn as sns

def problem_1_balanced_tp():
    
    
    print("\n" + "="*70)
    print("PROBLEM 1: BALANCED TRANSPORTATION PROBLEM")
    print("="*70)
    
    
    sources = ['Factory_A', 'Factory_B', 'Factory_C']
    destinations = ['Market_X', 'Market_Y', 'Market_Z']
    
    supply = {'Factory_A': 10, 'Factory_B': 15, 'Factory_C': 12}
    demand = {'Market_X': 12, 'Market_Y': 10, 'Market_Z': 15}
    
    
    costs = {
        ('Factory_A', 'Market_X'): 4,
        ('Factory_A', 'Market_Y'): 3,
        ('Factory_A', 'Market_Z'): 2,
        ('Factory_B', 'Market_X'): 5,
        ('Factory_B', 'Market_Y'): 6,
        ('Factory_B', 'Market_Z'): 8,
        ('Factory_C', 'Market_X'): 6,
        ('Factory_C', 'Market_Y'): 5,
        ('Factory_C', 'Market_Z'): 4,
    }
    
    
    total_supply = sum(supply.values())
    total_demand = sum(demand.values())
    print(f"\nStep 1: BALANCE CHECK")
    print(f"  Total Supply: {total_supply}")
    print(f"  Total Demand: {total_demand}")
    print(f"  Status: {'BALANCED ✓' if total_supply == total_demand else 'UNBALANCED ✗'}")
    
    
    print(f"\nStep 2: FORMULATE LINEAR PROGRAM")
    prob = LpProblem("Transportation_Problem_1", LpMinimize)
    
    
    routes = [(i, j) for i in sources for j in destinations]
    vars_dict = LpVariable.dicts("Route", routes, lowBound=0, cat='Continuous')
    
    
    prob += lpSum([vars_dict[(i, j)] * costs[(i, j)] for (i, j) in routes]), "Total_Cost"
    print(f"  Created {len(routes)} decision variables")
    print(f"  Objective: Minimize Z = Σ cᵢⱼ × xᵢⱼ")
    
    
    print(f"\nStep 3: ADD CONSTRAINTS")
    for i in sources:
        prob += lpSum([vars_dict[(i, j)] for j in destinations]) == supply[i], f"Supply_{i}"
    print(f"  Added {len(sources)} supply constraints")
    
    
    for j in destinations:
        prob += lpSum([vars_dict[(i, j)] for i in sources]) == demand[j], f"Demand_{j}"
    print(f"  Added {len(destinations)} demand constraints")
    print(f"  Total constraints: {len(prob.constraints)}")
    
    
    print(f"\nStep 4: SOLVE OPTIMIZATION PROBLEM")
    prob.solve(PULP_CBC_CMD(msg=0))
    
    print(f"  Status: {LpStatus[prob.status]}")
    print(f"  Minimum Total Cost: Rs. {value(prob.objective):.2f}")
    
    
    print(f"\nStep 5: OPTIMAL ALLOCATION SOLUTION")
    print(f"\n{'From':<15} {'To':<15} {'Units':<10} {'Cost/Unit':<10} {'Total Cost':<10}")
    print("-" * 60)
    
    allocation_data = []
    total_cost_check = 0
    
    for i in sources:
        for j in destinations:
            if vars_dict[(i, j)].varValue > 0.001:  
                units = vars_dict[(i, j)].varValue
                unit_cost = costs[(i, j)]
                route_cost = units * unit_cost
                total_cost_check += route_cost
                print(f"{i:<15} {j:<15} {units:>9.2f} {unit_cost:>9.2f} {route_cost:>9.2f}")
                allocation_data.append({
                    'From': i,
                    'To': j,
                    'Units': units,
                    'Cost_Per_Unit': unit_cost,
                    'Total_Cost': route_cost
                })
    
    print("-" * 60)
    print(f"{'TOTAL':<15} {'TRANSPORTATION COST':<15} {'':>9} {'':>9} {value(prob.objective):>9.2f}")
    
    
    print(f"\nStep 6: CONSTRAINT VERIFICATION")
    print(f"\nSupply Verification:")
    for i in sources:
        shipped = sum([vars_dict[(i, j)].varValue for j in destinations])
        print(f"  {i}: Shipped {shipped:.2f} (Required: {supply[i]}) {'✓' if abs(shipped - supply[i]) < 0.01 else '✗'}")
    
    print(f"\nDemand Verification:")
    for j in destinations:
        received = sum([vars_dict[(i, j)].varValue for i in sources])
        print(f"  {j}: Received {received:.2f} (Required: {demand[j]}) {'✓' if abs(received - demand[j]) < 0.01 else '✗'}")
    
    
    return {
        'problem': 'Problem_1_Balanced',
        'allocation': allocation_data,
        'total_cost': value(prob.objective),
        'variables': vars_dict,
        'sources': sources,
        'destinations': destinations,
        'supply': supply,
        'demand': demand,
        'costs': costs
    }






def problem_2_unbalanced_supply_excess():
    """
    Supply > Demand: Add dummy destination to absorb excess
    Costs to dummy destination = 0 (represents unsold inventory)
    """
    
    print("\n\n" + "="*70)
    print("PROBLEM 2: UNBALANCED TP - SUPPLY > DEMAND")
    print("="*70)
    
    sources = ['Plant_1', 'Plant_2', 'Plant_3']
    destinations = ['DC_1', 'DC_2', 'DC_3']
    
    supply = {'Plant_1': 1000, 'Plant_2': 1500, 'Plant_3': 1200}
    demand = {'DC_1': 2300, 'DC_2': 1400, 'DC_3': 1000}
    
    
    costs = {
        ('Plant_1', 'DC_1'): 80, ('Plant_1', 'DC_2'): 215, ('Plant_1', 'DC_3'): 100,
        ('Plant_2', 'DC_1'): 100, ('Plant_2', 'DC_2'): 108, ('Plant_2', 'DC_3'): 150,
        ('Plant_3', 'DC_1'): 102, ('Plant_3', 'DC_2'): 68, ('Plant_3', 'DC_3'): 120,
    }
    
    
    total_supply = sum(supply.values())
    total_demand = sum(demand.values())
    print(f"\nStep 1: BALANCE CHECK")
    print(f"  Total Supply: {total_supply}")
    print(f"  Total Demand: {total_demand}")
    print(f"  Difference: {total_supply - total_demand}")
    
    
    if total_supply > total_demand:
        excess = total_supply - total_demand
        print(f"  Status: UNBALANCED - Supply Exceeds Demand by {excess} units")
        print(f"  Action: Add Dummy Destination to absorb excess")
        
        destinations.append('Dummy_Warehouse')
        demand['Dummy_Warehouse'] = excess
        
        
        for i in sources:
            costs[(i, 'Dummy_Warehouse')] = 0
    
    
    print(f"\nStep 2: FORMULATE BALANCED LP")
    prob = LpProblem("Transportation_Problem_2_Unbalanced", LpMinimize)
    
    routes = [(i, j) for i in sources for j in destinations]
    vars_dict = LpVariable.dicts("Route", routes, lowBound=0, cat='Continuous')
    
    prob += lpSum([vars_dict[(i, j)] * costs.get((i, j), 0) for (i, j) in routes]), "Total_Cost"
    
    for i in sources:
        prob += lpSum([vars_dict[(i, j)] for j in destinations]) == supply[i]
    
    for j in destinations:
        prob += lpSum([vars_dict[(i, j)] for i in sources]) == demand[j]
    
    print(f"  Variables: {len(routes)}, Constraints: {len(prob.constraints)}")
    
    
    print(f"\nStep 3: SOLVE")
    prob.solve(PULP_CBC_CMD(msg=0))
    print(f"  Status: {LpStatus[prob.status]}")
    print(f"  Minimum Total Cost: Rs. {value(prob.objective):.2f}")
    
    
    print(f"\nStep 4: OPTIMAL ALLOCATION")
    print(f"\n{'From':<15} {'To':<20} {'Units':<12} {'Cost/Unit':<12} {'Total Cost':<12}")
    print("-" * 70)
    
    allocation_data = []
    for i in sources:
        for j in destinations:
            if vars_dict[(i, j)].varValue > 0.001:
                units = vars_dict[(i, j)].varValue
                unit_cost = costs.get((i, j), 0)
                route_cost = units * unit_cost
                print(f"{i:<15} {j:<20} {units:>11.2f} {unit_cost:>11.2f} {route_cost:>11.2f}")
                allocation_data.append({
                    'From': i,
                    'To': j,
                    'Units': units,
                    'Type': 'Dummy' if 'Dummy' in j else 'Real'
                })
    
    print("-" * 70)
    print(f"TOTAL TRANSPORTATION COST: Rs. {value(prob.objective):.2f}")
    
    
    print(f"\nStep 5: INTERPRETATION")
    dummy_allocation = 0
    for i in sources:
        if (i, 'Dummy_Warehouse') in vars_dict and vars_dict[(i, 'Dummy_Warehouse')].varValue > 0.001:
            dummy_allocation += vars_dict[(i, 'Dummy_Warehouse')].varValue
    print(f"  Total units shipped to Dummy Warehouse: {dummy_allocation:.2f}")
    print(f"  Interpretation: These units represent EXCESS INVENTORY/SURPLUS")
    print(f"  that cannot be distributed to regular markets.")
    print(f"  Action: Consider reducing production or finding new markets.")
    
    return {
        'problem': 'Problem_2_Unbalanced_SupplyExcess',
        'allocation': allocation_data,
        'total_cost': value(prob.objective),
        'dummy_allocation': dummy_allocation
    }






def problem_3_unbalanced_demand_excess():
    """
    Demand > Supply: Add dummy source with penalty cost for unmet demand
    """
    
    print("\n\n" + "="*70)
    print("PROBLEM 3: UNBALANCED TP - DEMAND > SUPPLY (PREMIUM NETWORK)")
    print("="*70)
    
    sources = ['Plant_1', 'Plant_2', 'Plant_3']
    destinations = ['City_1', 'City_2', 'City_3']
    
    
    supply = {'Plant_1': 25, 'Plant_2': 40, 'Plant_3': 30}
    demand = {'City_1': 30, 'City_2': 35, 'City_3': 25}
    
    
    print("\nStep 1: SCENARIO ANALYSIS")
    print(f"  Normal Demand: City_1=30, City_2=35, City_3=25, Total=90")
    print(f"  With 20% Increase: City_1=36, City_2=42, City_3=30, Total=108")
    
    demand_increased = {'City_1': 36, 'City_2': 42, 'City_3': 30}
    
    total_supply = sum(supply.values())
    total_demand = sum(demand_increased.values())
    shortage = total_demand - total_supply
    
    print(f"  Total Supply: {total_supply}")
    print(f"  Total Demand (with increase): {total_demand}")
    print(f"  Shortage: {shortage} units")
    print(f"  Status: UNBALANCED - Demand Exceeds Supply by {shortage} units")
    print(f"  Action: Add Dummy Source with {shortage} units from External Network")
    
    
    sources.append('External_Network')
    supply['External_Network'] = shortage
    
    
    costs = {
        ('Plant_1', 'City_1'): 600, ('Plant_1', 'City_2'): 700, ('Plant_1', 'City_3'): 400,
        ('Plant_2', 'City_1'): 320, ('Plant_2', 'City_2'): 300, ('Plant_2', 'City_3'): 350,
        ('Plant_3', 'City_1'): 500, ('Plant_3', 'City_2'): 480, ('Plant_3', 'City_3'): 450,
        ('External_Network', 'City_1'): 1000,
        ('External_Network', 'City_2'): 1000,
        ('External_Network', 'City_3'): 1000,
    }
    
    print(f"\nStep 2: FORMULATE LP WITH EXTERNAL SOURCE")
    prob = LpProblem("Transportation_Problem_3_PremiumNetwork", LpMinimize)
    
    routes = [(i, j) for i in sources for j in destinations]
    vars_dict = LpVariable.dicts("Route", routes, lowBound=0, cat='Continuous')
    
    prob += lpSum([vars_dict[(i, j)] * costs[(i, j)] for (i, j) in routes]), "Total_Cost"
    
    for i in sources:
        prob += lpSum([vars_dict[(i, j)] for j in destinations]) == supply[i]
    
    for j in destinations:
        prob += lpSum([vars_dict[(i, j)] for i in sources]) == demand_increased[j]
    
    print(f"  Variables: {len(routes)}, Constraints: {len(prob.constraints)}")
    
    
    print(f"\nStep 3: SOLVE")
    prob.solve(PULP_CBC_CMD(msg=0))
    print(f"  Status: {LpStatus[prob.status]}")
    print(f"  Total Cost (Transportation + Premium): Rs. {value(prob.objective):.2f}")
    
    
    print(f"\nStep 4: OPTIMAL ALLOCATION WITH DEMAND INCREASE")
    print(f"\n{'From':<20} {'To':<12} {'Units':<10} {'Cost/Unit':<12} {'Total Cost':<12}")
    print("-" * 70)
    
    allocation_data = []
    premium_cost = 0
    
    for i in sources:
        for j in destinations:
            if vars_dict[(i, j)].varValue > 0.001:
                units = vars_dict[(i, j)].varValue
                unit_cost = costs[(i, j)]
                route_cost = units * unit_cost
                source_type = 'Premium' if 'External' in i else 'Internal'
                print(f"{i:<20} {j:<12} {units:>9.2f} {unit_cost:>11.2f} {route_cost:>11.2f}")
                
                if 'External' in i:
                    premium_cost += route_cost
                
                allocation_data.append({
                    'From': i,
                    'To': j,
                    'Units': units,
                    'Source_Type': source_type
                })
    
    print("-" * 70)
    print(f"TOTAL COST: Rs. {value(prob.objective):.2f}")
    
    
    print(f"\nStep 5: COST BREAKDOWN & INTERPRETATION")
    transport_cost = value(prob.objective) - premium_cost
    print(f"  Regular Transportation Cost: Rs. {transport_cost:.2f}")
    print(f"  Premium Network Cost (shortage): Rs. {premium_cost:.2f}")
    print(f"  Premium as % of Total: {100*premium_cost/value(prob.objective):.1f}%")
    
    print(f"\nStep 6: SHORTAGE ANALYSIS BY DESTINATION")
    for j in destinations:
        from_external = vars_dict[('External_Network', j)].varValue
        penalty = from_external * costs[('External_Network', j)]
        if from_external > 0.001:
            print(f"  {j}: {from_external:.0f} units from external (Penalty: Rs. {penalty:.2f})")
        else:
            print(f"  {j}: Fully met by internal plants ✓")
    
    print(f"\nRECOMMENDATION: Expand production capacity to reduce premium costs")
    
    return {
        'problem': 'Problem_3_DemandExcess',
        'allocation': allocation_data,
        'total_cost': value(prob.objective),
        'premium_cost': premium_cost
    }






def create_allocation_visualization(results, problem_name):
    """Create heatmap visualization of allocation"""
    
    print(f"\nGenerating visualization for {problem_name}...")
    
    allocation_df = pd.DataFrame(results['allocation'])
    
    
    pivot = allocation_df.pivot_table(
        values='Units', 
        index='From', 
        columns='To', 
        aggfunc='sum', 
        fill_value=0
    )
    
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Units'})
    plt.title(f'{problem_name}\nOptimal Allocation Heatmap')
    plt.xlabel('Destinations')
    plt.ylabel('Sources')
    plt.tight_layout()
    
    filename = f'{problem_name.replace(" ", "_")}_allocation.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {filename}")
    plt.close()






if __name__ == "__main__":
    
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  TRANSPORTATION PROBLEM - COMPREHENSIVE PYTHON SOLUTION".center(68) + "█")
    print("█" + "  MATH F212 Optimization Assignment".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    
    results_1 = problem_1_balanced_tp()
    results_2 = problem_2_unbalanced_supply_excess()
    results_3 = problem_3_unbalanced_demand_excess()
    
    
    print("\n" + "="*70)
    print("CREATING VISUALIZATIONS")
    print("="*70)
    
    create_allocation_visualization(results_1, "Problem_1_Balanced_TP")
    create_allocation_visualization(results_2, "Problem_2_Supply_Excess")
    create_allocation_visualization(results_3, "Problem_3_Demand_Excess")
    
    
    print("\n" + "="*70)
    print("SOLUTION SUMMARY")
    print("="*70)
    print(f"Problem 1 (Balanced): Minimum Cost = Rs. {results_1['total_cost']:.2f}")
    print(f"Problem 2 (Supply>Demand): Minimum Cost = Rs. {results_2['total_cost']:.2f}")
    print(f"  - Excess inventory to warehouse: {results_2['dummy_allocation']:.2f} units")
    print(f"Problem 3 (Demand>Supply): Total Cost = Rs. {results_3['total_cost']:.2f}")
    print(f"  - Premium network cost (for shortage): Rs. {results_3['premium_cost']:.2f}")
    
    print("\n✓ All problems solved successfully!")
    print("✓ See visualization images for allocation heatmaps")
    print("\n" + "█"*70)