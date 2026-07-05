# PowerShell script to build the Rust library for quantum storage

Write-Host "Building Quantum Storage Rust Library..." -ForegroundColor Green

# Navigate to the source directory
Set-Location -Path "c:\quantum-devops-project\src\core"

# Create Cargo.toml if it doesn't exist
$CargoTomlContent = @'
[package]
name = "quantum_storage_rust"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
'@

if (-not (Test-Path "Cargo.toml")) {
    Write-Host "Creating Cargo.toml..." -ForegroundColor Yellow
    Set-Content -Path "Cargo.toml" -Value $CargoTomlContent
}

# Build the library
Write-Host "Compiling Rust library..." -ForegroundColor Yellow
cargo build --release

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Library located at: target\release\quantum_storage_rust.dll" -ForegroundColor Cyan
} else {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

# Copy the DLL to a location where C# can find it
Copy-Item -Path "target\release\quantum_storage_rust.dll" -Destination "..\..\lib\quantum_storage_rust.dll" -Force
Write-Host "Copied DLL to lib directory" -ForegroundColor Green

Write-Host "Quantum Storage Rust Library build complete!" -ForegroundColor Green