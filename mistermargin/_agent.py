import uuid
from abc import ABCMeta, abstractmethod


class Agent(metaclass=ABCMeta):

  def __init__(self):
    self.id = str(uuid.uuid4())
    self.feed: "Feed"

  @abstractmethod
  def data(self):
    """
    Initialize the agent.
    Override this method.
    Declare attributes.
    """

  @abstractmethod
  def next(self):
    """
    Main agent runtime method.
    Called as each new step becomes available.
    """
