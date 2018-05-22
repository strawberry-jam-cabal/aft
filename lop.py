# helper for intelligently accumulating results
def add_result(typeAccum, typeAnnotation, instance):
    if not(typeAnnotation in (map(lambda x: x[0], typeAccum))):
        typeAccum.append((typeAnnotation, instance))

def show_results(typeAccum):
    for (typeAnnotation, inst) in typeAccum:
        print(typeAnnotation+ "│", inst)


