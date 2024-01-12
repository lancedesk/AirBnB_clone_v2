# AirBnB Clone

This project is an implementation of a simplified AirBnB clone, including a command-line console, file storage, and various model classes.

## Project Structure

The project is organized into the following directories and files:

- **models/**: Contains the various model classes.
  - `base_model.py`: Defines the BaseModel class.
  - `user.py`: Defines the User class.
  - `state.py`, `city.py`, `amenity.py`, `place.py`, `review.py`: Other model classes.
  - `engine/`: Contains the file storage implementation.
    - `__init__.py`: Initializes the storage engine.
    - `file_storage.py`: Defines the FileStorage class.
- **tests/**: Contains test files (if any).
- **console.py**: Command-line console implementation.

## Getting Started

To run the console and interact with the AirBnB clone, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/AirBnB_clone.git
   cd AirBnB_clone
   ```

2. Run the console:

   ```bash
   ./console.py
   ```

   The console will start, allowing you to perform various actions on the models.

## Console Commands

The console supports the following commands:

- `help`: Display help messages.
- `quit` or `EOF`: Quit the console.
- `create`: Create a new instance of a model.
- `show`: Display the string representation of an instance.
- `destroy`: Delete an instance based on the class name and ID.
- `all`: Display the string representation of all instances.
- `update`: Update an instance based on the class name and ID.

## Model Classes

- **BaseModel**: The base class for other model classes.
- **User**: Represents a user.
- **State, City, Amenity, Place, Review**: Other model classes.
