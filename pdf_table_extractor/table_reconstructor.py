class TableReconstructor:
     #This function calculates the vertical center (Y position) of a word.
     #bbox = 4 corners of a rectangle
     #Each p[1] = Y coordinate of a corner
    def center_y(self, bbox):
        return sum(p[1] for p in bbox) / 4
   
    def build_table(self, words):
 
        rows = []
        #Sort words top → bottom
        words = sorted(
            words,
            key=lambda x: self.center_y(
                x["bbox"]
            )
        )
        #Words within 20 pixels vertically are considered same row.
        tolerance = 20
 
        for word in words:
 
            y = self.center_y(word["bbox"])
 
            found = False
 
            for row in rows:
 
                if abs(row["y"] - y) < tolerance:
                    row["cells"].append(word)
                    found = True
                    break
 
            if not found:
 
                rows.append({"y": y,"cells": [word]})
 
        return rows