package com.codedock.dto;

import com.codedock.entity.Program;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProgramResponse {

    private Long id;
    private String language;
    private String title;
    private String code;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static ProgramResponse fromEntity(Program program) {
        return ProgramResponse.builder()
                .id(program.getId())
                .language(program.getLanguage())
                .title(program.getTitle())
                .code(program.getCode())
                .createdAt(program.getCreatedAt())
                .updatedAt(program.getUpdatedAt())
                .build();
    }
}