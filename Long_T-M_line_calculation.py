"""
Long Transmission Line Analysis
================================

Power Systems-II | Electrical Engineering

This program calculates:
1. Series impedance per km
2. Shunt admittance per km
3. Propagation constant
4. Characteristic impedance
5. ABCD parameters
6. Sending-end voltage
7. Sending-end current
8. Voltage regulation
9. Sending-end power
10. Receiving-end power
11. Transmission efficiency

Method:
    Exact Long Transmission Line Method
"""

import cmath
import math


def polar_to_complex(magnitude, angle):
    """Convert polar form to rectangular complex form."""
    return cmath.rect(
        magnitude,
        math.radians(angle)
    )


def polar_form(value):
    """Return magnitude and angle of a complex value."""
    return abs(value), math.degrees(cmath.phase(value))


def calculate_line_parameters(
    resistance_per_km,
    reactance_per_km,
    capacitance_microfarad_per_km,
    frequency
):
    """Calculate Z' and Y' per kilometre."""

    # Series impedance per km
    z_per_km = complex(
        resistance_per_km,
        reactance_per_km
    )

    # Capacitance per km in farads
    capacitance = capacitance_microfarad_per_km * 1e-6

    # Angular frequency
    omega = 2 * math.pi * frequency

    # Shunt admittance per km
    y_per_km = complex(
        0,
        omega * capacitance
    )

    return z_per_km, y_per_km


def calculate_abcd(z_per_km, y_per_km, length):
    """Calculate ABCD parameters using exact long-line equations."""

    # Propagation constant
    gamma = cmath.sqrt(z_per_km * y_per_km)

    # Characteristic impedance
    zc = cmath.sqrt(z_per_km / y_per_km)

    # Electrical length
    gamma_l = gamma * length

    # ABCD parameters
    A = cmath.cosh(gamma_l)
    D = A

    B = zc * cmath.sinh(gamma_l)

    C = cmath.sinh(gamma_l) / zc

    return gamma, zc, A, B, C, D


def calculate_sending_end(Vr, Ir, A, B, C, D):
    """Calculate sending-end voltage and current."""

    Vs = A * Vr + B * Ir
    Is = C * Vr + D * Ir

    return Vs, Is


def main():

    print("=" * 70)
    print("          LONG TRANSMISSION LINE ANALYSIS")
    print("                  POWER SYSTEMS-II")
    print("             EXACT LONG-LINE METHOD")
    print("=" * 70)

    try:

        # ---------------- INPUT ----------------

        length = float(
            input("\nEnter transmission line length (km): ")
        )

        resistance_per_km = float(
            input("Enter resistance per km (ohm/km): ")
        )

        reactance_per_km = float(
            input("Enter reactance per km (ohm/km): ")
        )

        capacitance_per_km = float(
            input("Enter capacitance per km (microF/km): ")
        )

        frequency = float(
            input("Enter system frequency (Hz): ")
        )

        Vr_magnitude = float(
            input("Enter receiving-end voltage (V): ")
        )

        Vr_angle = float(
            input("Enter receiving-end voltage angle (degrees): ")
        )

        Ir_magnitude = float(
            input("Enter receiving-end current (A): ")
        )

        Ir_angle = float(
            input("Enter receiving-end current angle (degrees): ")
        )

        # ---------------- VALIDATION ----------------

        if length <= 0:
            raise ValueError(
                "Line length must be greater than zero."
            )

        if resistance_per_km < 0:
            raise ValueError(
                "Resistance cannot be negative."
            )

        if reactance_per_km < 0:
            raise ValueError(
                "Reactance cannot be negative."
            )

        if capacitance_per_km < 0:
            raise ValueError(
                "Capacitance cannot be negative."
            )

        if frequency <= 0:
            raise ValueError(
                "Frequency must be greater than zero."
            )

        if Vr_magnitude <= 0:
            raise ValueError(
                "Receiving-end voltage must be greater than zero."
            )

        if Ir_magnitude < 0:
            raise ValueError(
                "Current cannot be negative."
            )

        # ---------------- RECEIVING-END PHASORS ----------------

        Vr = polar_to_complex(
            Vr_magnitude,
            Vr_angle
        )

        Ir = polar_to_complex(
            Ir_magnitude,
            Ir_angle
        )

        # ---------------- LINE PARAMETERS ----------------

        z_per_km, y_per_km = calculate_line_parameters(
            resistance_per_km,
            reactance_per_km,
            capacitance_per_km,
            frequency
        )

        # ---------------- ABCD PARAMETERS ----------------

        gamma, zc, A, B, C, D = calculate_abcd(
            z_per_km,
            y_per_km,
            length
        )

        # ---------------- SENDING-END VALUES ----------------

        Vs, Is = calculate_sending_end(
            Vr,
            Ir,
            A,
            B,
            C,
            D
        )

        # ---------------- POLAR VALUES ----------------

        gamma_mag, gamma_angle = polar_form(gamma)
        zc_mag, zc_angle = polar_form(zc)
        Vs_mag, Vs_angle = polar_form(Vs)
        Is_mag, Is_angle = polar_form(Is)

        # ---------------- POWER CALCULATIONS ----------------

        receiving_power = (
            3
            * abs(Vr)
            * abs(Ir)
            * math.cos(
                math.radians(Vr_angle - Ir_angle)
            )
        )

        sending_power = (
            3
            * abs(Vs)
            * abs(Is)
            * math.cos(
                math.radians(Vs_angle - Is_angle)
            )
        )

        # ---------------- VOLTAGE REGULATION ----------------

        voltage_regulation = (
            (abs(Vs) - abs(Vr))
            / abs(Vr)
        ) * 100

        # ---------------- EFFICIENCY ----------------

        if sending_power != 0:
            efficiency = (
                receiving_power / sending_power
            ) * 100
        else:
            efficiency = 0

        # ---------------- OUTPUT ----------------

        print("\n" + "=" * 70)
        print("                       RESULTS")
        print("=" * 70)

        print("\nLINE PARAMETERS")
        print("-" * 70)

        print(
            f"Series Impedance / km : "
            f"{z_per_km.real:.6f} + "
            f"j{z_per_km.imag:.6f} ohm/km"
        )

        print(
            f"Shunt Admittance / km : "
            f"{y_per_km.real:.6f} + "
            f"j{y_per_km.imag:.6f} S/km"
        )

        print("\nPROPAGATION PARAMETERS")
        print("-" * 70)

        print(
            f"Propagation Constant γ : "
            f"{gamma.real:.8f} + "
            f"j{gamma.imag:.8f} /km"
        )

        print(
            f"|γ|                    : "
            f"{gamma_mag:.8f}"
        )

        print(
            f"∠γ                     : "
            f"{gamma_angle:.4f} degrees"
        )

        print(
            f"Characteristic Impedance: "
            f"{zc.real:.4f} + "
            f"j{zc.imag:.4f} ohm"
        )

        print(
            f"|Zc|                    : "
            f"{zc_mag:.4f} ohm"
        )

        print(
            f"∠Zc                     : "
            f"{zc_angle:.4f} degrees"
        )

        print("\nABCD PARAMETERS")
        print("-" * 70)

        print(
            f"A = {A.real:.8f} + "
            f"j{A.imag:.8f}"
        )

        print(
            f"B = {B.real:.8f} + "
            f"j{B.imag:.8f} ohm"
        )

        print(
            f"C = {C.real:.8f} + "
            f"j{C.imag:.8f} S"
        )

        print(
            f"D = {D.real:.8f} + "
            f"j{D.imag:.8f}"
        )

        print("\nSENDING-END QUANTITIES")
        print("-" * 70)

        print(
            f"Sending-End Voltage : "
            f"{Vs_mag:.2f} ∠ "
            f"{Vs_angle:.2f}° V"
        )

        print(
            f"Sending-End Current : "
            f"{Is_mag:.2f} ∠ "
            f"{Is_angle:.2f}° A"
        )

        print("\nPOWER SYSTEM PERFORMANCE")
        print("-" * 70)

        print(
            f"Receiving-End Power : "
            f"{receiving_power:.2f} W"
        )

        print(
            f"Sending-End Power   : "
            f"{sending_power:.2f} W"
        )

        print(
            f"Voltage Regulation  : "
            f"{voltage_regulation:.2f} %"
        )

        print(
            f"Transmission Efficiency: "
            f"{efficiency:.2f} %"
        )

        print("=" * 70)

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
