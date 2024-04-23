class BayesianNetwork(object):

    def init(self, values):
        return (self.setValue("B", values[0], None, None) * self.setValue("E", values[1], None,None) * self.setValue("A|B,E",values[2],values[0],values[1]) * self.setValue("J|A", values[3], values[2], None) * self.setValue("M|A", values[4], values[2], None))

    def nextValues(self, values):
        if None in values:
            nones = values.index(None)
            next_items = list(values)
            next_items[nones] = True
            val1 = self.nextValues(next_items)
            next_items[nones] = False
            val2 = self.nextValues(next_items)
            return val1 + val2
        else:
            return self.init(values)

    def setValue(self, val, val1, val2, val3):
        if val == "B":
            if val1:
                return 0.001
            else:
                return 0.999
        if val == "E":
            if val1:
                return 0.002
            else:
                return 0.998
        if val == "J|A":
            if val2:
                temp = 0.9
            else:
                temp = 0.05
            if val1:
                return temp
            else:
                return (1 - temp)
        if val == "M|A":
            if val2:
                temp = 0.7
            else:
                temp = 0.01
            if val1:
                return temp
            else:
                return (1 - temp)
        if val == "A|B,E":
            if val2 and val3:
                temp = 0.95
            if val2 and not val3:
                temp = 0.94
            if not val2 and val3:
                temp = 0.29
            if not val2 and not val3:
                temp = 0.001
            if val1:
                return temp
            else:
                return (1 - temp)

    def getValue(self, value):
        result = []
        if "Bt" in value:
            result.append(True)
        elif "Bf" in value:
            result.append(False)
        else:
            result.append(None)
        if "Et" in value:
            result.append(True)
        elif "Ef" in value:
            result.append(False)
        else:
            result.append(None)
        if "At" in value:
            result.append(True)
        elif "Af" in value:
            result.append(False)
        else:
            result.append(None)
        if "Jt" in value:
            result.append(True)
        elif "Jf" in value:
            result.append(False)
        else:
            result.append(None)
        if "Mt" in value:
            result.append(True)
        elif "Mf" in value:
            result.append(False)
        else:
            result.append(None)

        return result