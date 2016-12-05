class ExpertDoctor:

  def getVisitCost(self):
    return 40000

def validateVisitCost(cost):
  return cost < 30000

def test_answer():
  doc = ExpertDoctor()
  assert validateVisitCost(doc.getVisitCost())
