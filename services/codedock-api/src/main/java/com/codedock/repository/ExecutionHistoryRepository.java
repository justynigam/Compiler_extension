package com.codedock.repository;

import com.codedock.entity.ExecutionHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ExecutionHistoryRepository extends JpaRepository<ExecutionHistory, Long> {

    List<ExecutionHistory> findByProgramIdOrderByCreatedAtDesc(Long programId);
}