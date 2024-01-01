import pulp as p 
# Create a LP Minimization problem 
Lp_prob = p.LpProblem('Problem', sense = p.LpMinimize)  

x = p.LpVariable("x1", lowBound = 0)   # Create a variable x 
y = p.LpVariable("x2", lowBound = 0)

# Objective Function 
Lp_prob += x+y
# Constraints: 
Lp_prob += x+y==3

print(Lp_prob) 
status = Lp_prob.solve()   
print('Solution Status:')
print(p.LpStatus[status])   # The solution status 
print('###')

print('Optimal Solution:')
print([p.value(x), p.value(y)])
print('###')

print('Objective value:')
print(p.value(Lp_prob.objective))
print('###')

