from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import relationship
from db.base import Base


class LLM(Base):
    __tablename__ = "llms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    simulation_results = relationship("SimulationResult", back_populates="llm")
    rankings = relationship("Ranking", back_populates="llm")


class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    simulation_results = relationship("SimulationResult", back_populates="metric")
    rankings = relationship("Ranking", back_populates="metric")


class Simulation(Base):
    __tablename__ = "simulations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    seed = Column(Integer, nullable=True) 
    
    simulation_results = relationship("SimulationResult", back_populates="simulation")


class SimulationResult(Base):
    __tablename__ = "simulation_results"
    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    llm_id = Column(Integer, ForeignKey("llms.id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("metrics.id"), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    simulation = relationship("Simulation", back_populates="simulation_results")
    llm = relationship("LLM", back_populates="simulation_results")
    metric = relationship("Metric", back_populates="simulation_results")


class Ranking(Base):
    __tablename__ = "rankings"
    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(Integer, ForeignKey("metrics.id"), nullable=False)
    llm_id = Column(Integer, ForeignKey("llms.id"), nullable=False)
    mean_value = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)

    metric = relationship("Metric", back_populates="rankings")
    llm = relationship("LLM", back_populates="rankings")

    __table_args__ = (UniqueConstraint("metric_id", "llm_id", name="_metric_llm_uc"),)
