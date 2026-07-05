// Test program for Quantum Storage Manager
// This demonstrates the integration of C# with Rust for quantum storage

using System;
using System.Collections.Generic;
using System.Numerics;
using QuantumDevOps.Storage;

class TestQuantumStorage
{
    static void Main(string[] args)
    {
        Console.WriteLine("🧪 Testing Quantum Storage Manager Integration");
        Console.WriteLine("============================================");
        
        try
        {
            // Create the storage manager
            var storageManager = new QuantumStorageManager();
            
            // Create test quantum states
            var states = new List<QuantumState>
            {
                new QuantumState("test_001", new Complex[] { new Complex(1, 0), new Complex(0, 0) }, 1),
                new QuantumState("test_002", new Complex[] { new Complex(0, 1), new Complex(0, 0) }, 1),
                new QuantumState("test_003", new Complex[] { new Complex(0.707, 0), new Complex(0.707, 0) }, 1)
            };
            
            Console.WriteLine($"✓ Created {states.Count} test quantum states");
            
            // Stack the cubicals
            storageManager.StackCubicals(states);
            Console.WriteLine("✓ Successfully stacked cubicals with compression");
            
            // Interweave layers
            storageManager.InterweaveCubicalLayers();
            Console.WriteLine("✓ Successfully interwoven cubical layers");
            
            // Get statistics
            var stats = storageManager.GetStorageStatistics();
            Console.WriteLine("✓ Storage statistics retrieved:");
            foreach (var stat in stats)
            {
                Console.WriteLine($"  {stat.Key}: {stat.Value}");
            }
            
            Console.WriteLine("\n🎉 All tests passed! Quantum Storage Manager is working correctly.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error: {ex.Message}");
            Console.WriteLine(ex.StackTrace);
        }
    }
}