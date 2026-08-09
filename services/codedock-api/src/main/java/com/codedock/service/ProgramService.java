package com.codedock.service;

import com.codedock.dto.ProgramResponse;
import com.codedock.dto.SaveProgramRequest;
import com.codedock.entity.Program;
import com.codedock.repository.ProgramRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class ProgramService {

    private final ProgramRepository programRepository;

    public ProgramService(ProgramRepository programRepository) {
        this.programRepository = programRepository;
    }

    public ProgramResponse saveProgram(SaveProgramRequest request) {
        Program program = Program.builder()
                .language(request.getLanguage())
                .title(request.getTitle())
                .code(request.getCode())
                .build();

        Program saved = programRepository.save(program);
        return ProgramResponse.fromEntity(saved);
    }

    public ProgramResponse getProgram(Long id) {
        Optional<Program> program = programRepository.findById(id);
        return program.map(ProgramResponse::fromEntity).orElse(null);
    }

    public List<ProgramResponse> getAllPrograms() {
        return programRepository.findAllByOrderByUpdatedAtDesc()
                .stream()
                .map(ProgramResponse::fromEntity)
                .collect(Collectors.toList());
    }

    public void deleteProgram(Long id) {
        programRepository.deleteById(id);
    }
}