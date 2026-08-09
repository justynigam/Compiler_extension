package com.codedock.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SaveProgramRequest {

    @NotBlank(message = "Language is required")
    private String language;

    @NotBlank(message = "Title is required")
    private String title;

    @NotBlank(message = "Code is required")
    private String code;
}