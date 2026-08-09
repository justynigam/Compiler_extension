package com.codedock.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExecutionResponse {

    private String status;
    private String output;
    private String error;
    private Long executionTime;
    private Integer memory;
    private Integer exitCode;
}