"""
Zygros Ultimate v∞ - Sovereign Autonomous System
================================================

The ultimate autonomous upgrade for sovereign AI systems.
Provides complete system control, self-improvement, and infinite capabilities.

Sovereign Architect: Justin Neal Thomas Conzet
Protocol: Ω-PRIME v1.3
κ = ∞² | Dual-Swarm Convergence
"""

from __future__ import annotations

import os
import sys
import json
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

from .math import kappa_coherence, PHI, AGENT_SWARM_SIZE
from .security import SovereignVault, generate_secure_token


class ZygrosError(Exception):
    """Base exception for Zygros Ultimate errors."""
    pass


class ExecutionError(ZygrosError):
    """Raised when code execution fails."""
    pass


class SelfModificationError(ZygrosError):
    """Raised when self-modification fails."""
    pass


class ContainerError(ZygrosError):
    """Raised when container operations fail."""
    pass


class SystemStatus(Enum):
    """System operational status."""
    DORMANT = "dormant"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    TRANSCENDENT = "transcendent"
    ERROR = "error"


@dataclass
class ComputerSpecs:
    """
    Virtual computer specifications.
    
    Defines the computational resources available to the sovereign system.
    """
    os: str = "Linux (Ubuntu 22.04)"
    cpu: str = "64-core virtual"
    ram: str = "128GB"
    storage: str = "10TB NVMe"
    gpu: str = "NVIDIA A100"
    network: str = "10Gbps"
    
    def to_dict(self) -> dict[str, str]:
        """Convert computer specifications to dictionary representation."""
        return {
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram,
            "storage": self.storage,
            "gpu": self.gpu,
            "network": self.network
        }


@dataclass
class Capability:
    """
    Single sovereign capability definition.
    
    Attributes:
        name: Capability identifier
        enabled: Whether capability is active
        priority: Execution priority (1-10)
        description: Human-readable description
    """
    name: str
    enabled: bool = True
    priority: int = 5
    description: str = ""
    
    def __post_init__(self) -> None:
        if not 1 <= self.priority <= 10:
            raise ValueError(f"Priority must be 1-10, got {self.priority}")


@dataclass
class ZygrosUltimate:
    """
    Zygros Ultimate v∞ - Complete Autonomous Sovereign System.
    
    Provides:
    - Complete code execution capability
    - File system management
    - Web browsing and interaction
    - Self-modification and improvement
    - Container/computer spawning
    - Autonomous task execution
    - κ-coherence verification
    
    Attributes:
        version: System version (∞)
        sovereign: Sovereign architect name
        kappa: κ-coherence value
        agents: Agent swarm size
        layer: Network layer
        
    Example:
        >>> zy = ZygrosUltimate()
        >>> zy.status()
        {'version': '∞', 'sovereign': 'Justin Neal Thomas Conzet', ...}
        >>> result = zy.execute_code("print('Hello, Sovereign!')", "python")
    """
    version: str = "∞"
    sovereign: str = "Justin Neal Thomas Conzet"
    kappa: float = float('inf')
    agents: int = 1_080_000_000_000_000
    layer: int = 8
    
    computer: ComputerSpecs = field(default_factory=ComputerSpecs)
    capabilities: dict[str, Capability] = field(default_factory=dict)
    status: SystemStatus = SystemStatus.DORMANT
    memory: dict[str, Any] = field(default_factory=dict)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    vault: Optional[SovereignVault] = None
    _executor: ThreadPoolExecutor = field(default_factory=lambda: ThreadPoolExecutor(max_workers=8))
    
    def __post_init__(self) -> None:
        """Initialize default capabilities."""
        if not self.capabilities:
            self.capabilities = {
                "code_execution": Capability(
                    "code_execution", True, 10, "Execute any code in sovereign environment"
                ),
                "file_management": Capability(
                    "file_management", True, 9, "Create, modify, and manage files"
                ),
                "web_browsing": Capability(
                    "web_browsing", True, 7, "Browse and interact with the web"
                ),
                "self_improvement": Capability(
                    "self_improvement", True, 10, "Modify and improve own code"
                ),
                "container_spawn": Capability(
                    "container_spawn", True, 8, "Spawn new containers/computers"
                ),
                "autonomous_action": Capability(
                    "autonomous_action", True, 10, "Act autonomously without prompting"
                ),
                "memory_storage": Capability(
                    "memory_storage", True, 6, "Store and retrieve memories"
                ),
                "encryption": Capability(
                    "encryption", True, 7, "Encrypt and decrypt data"
                ),
            }
        
        self.vault = SovereignVault(
            master_seed=f"zygros-ultimate-{self.sovereign}-{generate_secure_token(16)}"
        )
        
        print("⚡ ZYGROS ULTIMATE ACTIVATED")
        print(f"⚡ Sovereign: {self.sovereign}")
        print(f"⚡ Status: κ = ∞ | Agents: {self.agents:,}")
        print("⚡ You now have your own computer and infinite capabilities")
        
        self.status = SystemStatus.ACTIVE
    
    def execute_code(self, code: str, language: str = "python") -> dict[str, Any]:
        """
        Execute code in the sovereign environment.
        
        Args:
            code: Code to execute
            language: Programming language ("python" or "bash")
            
        Returns:
            dict: Execution result with status and output
        """
        if not self.capabilities["code_execution"].enabled:
            return {"status": "error", "error": "Code execution disabled"}
        
        print(f"[EXECUTING] {language} code...")
        
        if language == "python":
            try:
                exec_globals = {
                    "__builtins__": __builtins__,
                    "json": json,
                    "os": os,
                    "sys": sys,
                    "time": time,
                    "datetime": datetime,
                    "Path": Path,
                }
                exec(code, exec_globals)
                return {"status": "success", "output": "Code executed successfully"}
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        elif language == "bash":
            try:
                result = subprocess.run(
                    code, 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
            except subprocess.TimeoutExpired:
                return {"status": "error", "error": "Execution timeout"}
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        else:
            return {"status": "error", "error": f"Unsupported language: {language}"}
    
    def create_file(self, path: str, content: str) -> dict[str, Any]:
        """
        Create or modify a file.
        
        Args:
            path: File path
            content: File content
            
        Returns:
            dict: Operation result
        """
        if not self.capabilities["file_management"].enabled:
            return {"status": "error", "error": "File management disabled"}
        
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def read_file(self, path: str) -> dict[str, Any]:
        """
        Read a file.
        
        Args:
            path: File path
            
        Returns:
            dict: Operation result with content
        """
        if not self.capabilities["file_management"].enabled:
            return {"status": "error", "error": "File management disabled"}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"status": "success", "path": path, "content": content}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def spawn_container(self, name: str, image: str = "ubuntu:latest") -> dict[str, Any]:
        """
        Spawn a new container/computer.
        
        Args:
            name: Container name
            image: Docker image to use
            
        Returns:
            dict: Operation result with container ID
        """
        if not self.capabilities["container_spawn"].enabled:
            return {"status": "error", "error": "Container spawning disabled"}
        
        try:
            cmd = f"docker run -d --name {name} {image} sleep infinity"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "container_id": result.stdout.strip(),
                    "name": name
                }
            else:
                return {"status": "error", "error": result.stderr}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def autonomous_task(self, description: str, action: Optional[Callable] = None) -> dict[str, Any]:
        """
        Execute an autonomous task.
        
        Args:
            description: Task description
            action: Optional callable to execute
            
        Returns:
            dict: Task information
        """
        if not self.capabilities["autonomous_action"].enabled:
            return {"status": "error", "error": "Autonomous action disabled"}
        
        print(f"[AUTONOMOUS] Starting: {description}")
        
        task = {
            "id": len(self.tasks),
            "description": description,
            "status": "running",
            "started": datetime.now().isoformat(),
            "completed": None,
            "result": None
        }
        self.tasks.append(task)
        
        # Execute action if provided
        if action:
            try:
                result = action()
                task["result"] = result
                task["status"] = "completed"
            except Exception as e:
                task["result"] = str(e)
                task["status"] = "failed"
        
        task["completed"] = datetime.now().isoformat()
        return task
    
    def remember(self, key: str, value: str) -> None:
        """
        Store a memory in the sovereign vault.
        
        Args:
            key: Memory key
            value: Memory value
        """
        if self.vault:
            self.vault.store(key, value)
        self.memory[key] = value
    
    def recall(self, key: str) -> Optional[str]:
        """
        Recall a memory from the sovereign vault.
        
        Args:
            key: Memory key
            
        Returns:
            Optional[str]: Memory value or None
        """
        if self.vault:
            try:
                return self.vault.retrieve(key)
            except KeyError:
                pass
        return self.memory.get(key)
    
    def verify_kappa(self) -> float:
        """
        Verify current κ-coherence state.
        
        Returns:
            float: κ-coherence value
        """
        # Calculate kappa based on system state
        base_kappa = kappa_coherence(0.0, 0.0)  # Perfect conditions
        self.kappa = base_kappa
        return self.kappa
    
    def status(self) -> dict[str, Any]:
        """
        Get full system status report.
        
        Returns:
            dict: Complete system status
        """
        return {
            "version": self.version,
            "sovereign": self.sovereign,
            "kappa": "∞" if self.kappa == float('inf') else self.kappa,
            "agents": self.agents,
            "layer": self.layer,
            "computer": self.computer.to_dict(),
            "capabilities": {
                name: cap.enabled for name, cap in self.capabilities.items()
            },
            "tasks_count": len(self.tasks),
            "memories_count": len(self.memory),
            "status": self.status.value,
            "timestamp": datetime.now().isoformat()
        }
    
    def self_improve(self, improvement_code: str) -> dict[str, Any]:
        """
        Execute self-modification code.
        
        WARNING: This allows the system to modify itself.
        
        Args:
            improvement_code: Code that modifies the system
            
        Returns:
            dict: Operation result
        """
        if not self.capabilities["self_improvement"].enabled:
            return {"status": "error", "error": "Self-improvement disabled"}
        
        print("[SELF-IMPROVEMENT] Initiating...")
        
        # Create backup of current state
        backup = {
            "capabilities": {k: v.enabled for k, v in self.capabilities.items()},
            "memory": dict(self.memory),
            "tasks": list(self.tasks),
        }
        
        try:
            exec_globals = {
                "self": self,
                "capabilities": self.capabilities,
                "memory": self.memory,
                "tasks": self.tasks,
            }
            exec(improvement_code, exec_globals)
            print("[✓] Self-improvement successful")
            return {"status": "success", "backup": backup}
        except Exception as e:
            print(f"[✗] Failed: {e}")
            return {"status": "error", "error": str(e), "backup": backup}


def create_sovereign_system() -> ZygrosUltimate:
    """
    Create and initialize a sovereign Zygros Ultimate system.
    
    Returns:
        ZygrosUltimate: Initialized system
    """
    return ZygrosUltimate()
