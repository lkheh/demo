#include <iostream>
#include <windows.h>
#include <winternl.h>
#include <pe-parse/parse.h>

std::string base64_encode(const unsigned char* bytes_to_encode, unsigned int in_len) {
    const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    std::string ret;
    int i = 0;
    int j = 0;
    unsigned char char_array_3[3];
    unsigned char char_array_4[4];

    while (in_len--) {
        char_array_3[i++] = *(bytes_to_encode++));
        if (i == 3) {
            char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
            char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
            char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
            char_array_4[3] = char_array_3[2] & 0x3f;

            for (i = 0; (i < 4); i++) {
                ret += base64_chars[char_array_4[i]];
            }
            i = 0;
        }
    }

    if (i) {
        for (j = i; j < 3; j++) {
            char_array_3[j] = '\0';
        }

        char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
        char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
        char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
        char_array_4[3] = char_array_3[2] & 0x3f;

        for (j = 0; (j < i + 1); j++) {
            ret += base64_chars[char_array_4[j]];
        }

        while ((i++ < 3)) {
            ret += '=';
        }
    }

    return ret;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <pe_file_path> <section_name>" << std::endl;
        return 1;
    }

    pe_parse::pe_image pe_image(argv[1]);

    if (!pe_image.has_error()) {
        pe_parse::section_iterator section_iterator = pe_image.section_begin();

        while (section_iterator != pe_image.section_end()) {
            if (section_iterator->name() == argv[2]) {
                std::vector<uint8_t> section_data(section_iterator->virtual_size(), 0);

                if (section_iterator->virtual_size() > section_iterator->raw_size()) {
                    std::cerr << "Warning: Section has more virtual size than raw size." << std::endl;
                }

                if (pe_image.mmap(nullptr, image.size(), PROT_READ, MAP_PRIVATE, fd, 0)) 
				{
                    std::cerr << "Error: Failed to mmap the file." << std::endl;
                    return 1;
                }

                pe_parse::pe_image pe_image(image.data(), image.size(), pe_parse::pe_image_options::valid_segment_required);

                if (!pe_image.has_error()) {
                    pe_parse::section_iterator section_iterator = pe_image.section_begin();

                    while (section_iterator != pe_image.section_end()) {
                        if (section_iterator->name() == argv[2]) {
                            std::vector<uint8_t> section_data(section_iterator->virtual_size(), 0);

                            if (section_iterator->virtual_size() > section_iterator->raw_size()) {
                                std::cerr << "Warning: Section has more virtual size than raw size." << std::endl;
                            }

                            if (munmap(image.data(), image.size()) != 0) {
                                std::cerr << "Error: Failed to munmap the file." << std::endl;
                                return 11;
                            }

                            // Encode the data to Base64
                            std::string base64 = base64_encode(section_data.data(), section_data.size());
                            std::cout << "Base64 encoded data: " << base64 << std::endl;

                            return 0;
                        }

                        ++section_iterator;
                    }

                    std::cerr << "Error: Section not found." << std::endl;
                    return 11;
                } else {
                    std::cerr << "Error: Failed to parse the PE image." << std::endl;
                    return 11;
                }
            }

            ++section_iterator;
        }

        std::cerr << "Error: Section not found." << std::endl;
        return 11;
    } else {
        std::cerr << "Error: Failed to open the file." << std::endl;
        return 11;
    }
}
