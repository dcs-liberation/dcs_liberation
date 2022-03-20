from dataclasses import dataclass, field
from typing import List

from game.ato.package import Package


@dataclass
class AirTaskingOrder:
    """The entire ATO for one coalition."""

    #: The set of all planned packages in the ATO.
    packages: List[Package] = field(default_factory=list)

    def add_package(self, package: Package) -> None:
        """Adds a package to the ATO."""
        self.packages.append(package)

    def remove_package(self, package: Package) -> None:
        """Removes a package from the ATO."""
        # Remove all the flights individually so the database gets updated.
        for flight in list(package.flights):
            package.remove_flight(flight)
        self.packages.remove(package)

    def clear(self) -> None:
        """Removes all packages from the ATO."""
        # Remove all packages individually so the database gets updated.
        for package in list(self.packages):
            self.remove_package(package)
