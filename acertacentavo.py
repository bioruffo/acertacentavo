# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 09:13:41 2019

@author: roberto.rosati

USE ONLINE:
https://repl.it/@RobertoRosati/acertacentavo

"""
# 1) No Repl.it, copie e cole aqui (do excel) os valores para usar,
#    as celas do excel devem estar no formato:
#    <nome> <tamanho da unidade> <custo unitario>
custos_import = '''
Rack 10ul	1	 R$ 27,49 
Rack 100ul	1	 R$ 27,30 
Rack 1000 ul	1	 R$ 25,85 
Tubos 15ml	100	 R$ 64,26 
Tubos 50ml	20	 R$ 15,66 
Oligo (bases)	1	 R$ 1,76 
eppendorf Low retention	250	 R$ 35,50 
Eppendorf	500	 R$ 40,60 
'''

# 2) Coloque aqui o valor a ser atingido (sem IGP):
goal = '''
 R$ 734,11
'''

# 3) Escreva o numero maximo de itens diferentes em um combo
max_items = 3

# 4) No repl.it, aperte o botão "run" (acima)

# 5) Quando tiver resultados suficientes (se tiver), aperte "Stop"

# Esse é o IGP, se quiser mudar, tem que usar o ponto "." para decimal
igp = 0.0635




reallylong = 40


class AcertaCentavo:
    def __init__(self, costs_import, goal, igp, reallylong=40, max_items=6):
        self.igp=igp
        self.reallylong = reallylong
        self.costs = self.parse_costs(costs_import)
        self.maxlen = min(reallylong, max(len(n) for n in self.costs.keys()))
        self.print_costs()
    
        self.goal = [currency_to_float(value) \
                for value in goal.split('\n') if value !=''][0]
        print("\nGoal is: R$ {:.4f}".format(self.goal))
        self.max_items = max_items
        
        
    def do(self):
        print("\nLooking for combos with {} items maximum.".format(self.max_items))

        self.itemlist = list(self.costs.keys())
        self.ok = self.iteritems(self.goal)
        
        print ("\nI have found {} permutations.".format(len(self.ok)))
        
        if len(self.ok) == 0:
            print("I have found no combinations with a maximum of {} items.".format(\
                  self.max_items))
            
        
    def iteritems(self, left_money, curr_dict = None, itempos = 0, \
                  valid = None, min_items = [9999]):
        if itempos >= len(self.itemlist):
            return 2
        if curr_dict is None:
            curr_dict = ([(item, 0) for item in self.itemlist])
        if valid is None:
            valid = []
        itemname = self.itemlist[itempos]
        itemcost = self.costs[itemname]['cost']
        upper_bound = int(left_money/itemcost)
        if upper_bound <= 0:
            return 3
        else:
            for add in range(0, upper_bound+1):
                new_dict = dict(curr_dict)
                new_dict[itemname] = new_dict[itemname]+add
                new_money = left_money - itemcost*add
                if abs(new_money) <= 0.004:
                    possible = dict([(key, value) for key, value in new_dict.items() \
                                   if value > 0])
                    if min_items[0] > len(possible):
                        min_items[0] = len(possible)
                        if min_items[0] > max_items:
                            print("Smallest combo so far has {} items (too many)".format(min_items[0]))
                    
                    if len(possible) <= max_items:
                        valid.append(possible)
                        self.print_found(possible)
                    
                else:
                    self.iteritems(new_money, new_dict, itempos+1, \
                              valid, min_items)
        if itempos == 0:
            print("Done - smallest combo had {} items.".format(min_items[0]))
            return valid
                
                
    def print_found(self, item):
        itemset = set([n for n in item.keys() if item[n]>0])
        print("\n*** Found a combination with {} items ***".format( \
              len(itemset)))
        regrade3 = 0
        for entry in itemset:
            print(('{} {:>4}  {:>7.1f}  R$ {:>7.2f}').format( \
                  self.nicey(entry), \
                  item[entry], \
                  item[entry]*self.costs[entry]['size'], \
                  item[entry]*self.costs[entry]['cost']))
            regrade3 += item[entry]*self.costs[entry]['cost']
        print('Total: R$ {:.4f} (R$ {:.4f} with {:.3%} IGP)'.format( \
              regrade3, regrade3*(1+self.igp), self.igp))
        print()
    
    
  
    def parse_costs(self, costs_import):
        costs_import = [valor for valor in costs_import.split('\n') if valor !='']
        
        costs = {}
        for item in costs_import:
            desc, size, cost = item.split('\t')
            size = float(size)
            cost = currency_to_float(cost)
            costs[desc]={'size': size, 'cost': cost}
        return costs


    def print_costs(self):
        print("\nIterating through {} items:".format( \
              len(self.costs)-1))
        print(('{} {:<6}  {:<7}').format(self.nicey("Name"), "Size", "Cost"))
        for item, values in self.costs.items():
          print(('{} {:>6}  R$ {:>7.2f}').format(self.nicey(item), values['size'], \
                values['cost']))

    
    def nicey(self, entry):
      return '\n'.join([entry[i:i+self.reallylong].ljust(self.maxlen, '_') \
                        for i in range(0, len(entry), self.reallylong)])


# Helper functions
def currency_to_float(text):
    return float(text.replace("R$", "").strip().replace('.', '').replace(',', '.'))



if __name__ == '__main__':
    act = AcertaCentavo(custos_import, goal, igp, reallylong, max_items)
    act.do()
