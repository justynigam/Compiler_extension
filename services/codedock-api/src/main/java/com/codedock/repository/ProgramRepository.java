package com.codedock.repository;

import com.codedock.entity.Program;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProgramRepository extends JpaRepository<Program, Long> {

    List<Program> findByLanguage(String language);

    List<Program> findAllByOrderByUpdatedAtDesc();
}