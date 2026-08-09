package com.codedock.controller;

import com.codedock.dto.ExecutionRequest;
import com.codedock.dto.ExecutionResponse;
import com.codedock.dto.ProgramResponse;
import com.codedock.dto.SaveProgramRequest;
import com.codedock.service.ExecutionService;
import com.codedock.service.ProgramService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/compiler")
public class CompilerController {

    private final ExecutionService executionService;
    private final ProgramService programService;

    public CompilerController(ExecutionService executionService, ProgramService programService) {
        this.executionService = executionService;
        this.programService = programService;
    }

    @PostMapping("/run")
    public ResponseEntity<ExecutionResponse> runCode(@Valid @RequestBody ExecutionRequest request) {
        ExecutionResponse response = executionService.execute(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/save")
    public ResponseEntity<ProgramResponse> saveProgram(@Valid @RequestBody SaveProgramRequest request) {
        ProgramResponse response = programService.saveProgram(request);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProgramResponse> getProgram(@PathVariable Long id) {
        ProgramResponse response = programService.getProgram(id);
        if (response == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(response);
    }

    @GetMapping("/all")
    public ResponseEntity<List<ProgramResponse>> getAllPrograms() {
        List<ProgramResponse> programs = programService.getAllPrograms();
        return ResponseEntity.ok(programs);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProgram(@PathVariable Long id) {
        programService.deleteProgram(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "OK"));
    }
}