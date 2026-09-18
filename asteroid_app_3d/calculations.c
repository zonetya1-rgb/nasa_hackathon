#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_ROWS 500
#define G 6.67430e-11
#define EARTH_MASS 5.972e24
#define ASTEROID_DENSITY 3000
#define TNT_JOULES_PER_TON 4.184e9

typedef struct {
    char id[32];
    char name[128];
    char date[16];
    double diameter_m;
    double speed_kph;
    double miss_distance_km;
    int hazardous;
} Asteroid;

typedef struct {
    double mass_kg;
    double kinetic_energy_j;
    double gravitational_force_n;
    double tnt_equivalent_megatons;
} Physics;

int read_csv(const char *path, Asteroid *rows) {
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "Could not open %s\n", path);
        exit(1);
    }

    char line[512];
    fgets(line, sizeof(line), f);
    int count = 0;

    while (fgets(line, sizeof(line), f) && count < MAX_ROWS) {
        Asteroid a;
        char *token = strtok(line, ",");
        strncpy(a.id, token, sizeof(a.id) - 1);

        token = strtok(NULL, ",");
        strncpy(a.name, token, sizeof(a.name) - 1);

        token = strtok(NULL, ",");
        strncpy(a.date, token, sizeof(a.date) - 1);

        token = strtok(NULL, ","); a.diameter_m = atof(token);
        token = strtok(NULL, ","); a.speed_kph = atof(token);
        token = strtok(NULL, ","); a.miss_distance_km = atof(token);
        token = strtok(NULL, ","); a.hazardous = atoi(token);

        rows[count++] = a;
    }

    fclose(f);
    return count;
}

Physics compute_physics(Asteroid a) {
    Physics p;

    double radius_m = a.diameter_m / 2.0;
    double volume_m3 = (4.0 / 3.0) * M_PI * pow(radius_m, 3);
    p.mass_kg = volume_m3 * ASTEROID_DENSITY;

    double speed_ms = a.speed_kph * 1000.0 / 3600.0;
    p.kinetic_energy_j = 0.5 * p.mass_kg * pow(speed_ms, 2);

    double distance_m = a.miss_distance_km * 1000.0;
    p.gravitational_force_n = (G * EARTH_MASS * p.mass_kg) / pow(distance_m, 2);

    double tons_tnt = p.kinetic_energy_j / TNT_JOULES_PER_TON;
    p.tnt_equivalent_megatons = tons_tnt / 1e6;

    return p;
}

int main() {
    Asteroid rows[MAX_ROWS];
    int count = read_csv("data/asteroids.csv", rows);

    FILE *out = fopen("data/results.json", "w");
    if (!out) {
        fprintf(stderr, "Could not write data/results.json\n");
        return 1;
    }

    fprintf(out, "[\n");
    for (int i = 0; i < count; i++) {
        Physics p = compute_physics(rows[i]);

        fprintf(out,
            "  {\"id\": \"%s\", \"name\": \"%s\", \"date\": \"%s\", "
            "\"diameter_m\": %.2f, \"speed_kph\": %.2f, \"miss_distance_km\": %.2f, "
            "\"hazardous\": %s, "
            "\"mass_kg_est\": %.3e, \"kinetic_energy_j_est\": %.3e, "
            "\"gravitational_force_n_est\": %.3e, \"tnt_equivalent_megatons_est\": %.4f}%s\n",
            rows[i].id, rows[i].name, rows[i].date,
            rows[i].diameter_m, rows[i].speed_kph, rows[i].miss_distance_km,
            rows[i].hazardous ? "true" : "false",
            p.mass_kg, p.kinetic_energy_j, p.gravitational_force_n, p.tnt_equivalent_megatons,
            (i < count - 1) ? "," : ""
        );
    }
    fprintf(out, "]\n");

    fclose(out);
    printf("Wrote %d asteroids with physics estimates to data/results.json\n", count);
    return 0;
}