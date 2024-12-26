#include <iostream>
#include <string>
#include <map>
#include <fstream>
#include <sstream>
#include <vector>
#include <iomanip>

// 坐标的类
class coordinate
{
public:
    double x, y, z;
};

// 每一个残基的类
class GRO_reside
{
public:
    std::string resname;                 // 残基名(无前面的数字)
    std::vector<std::string> atom_name;  // 原子名数组
    std::vector<coordinate> coor_vector; // 原子坐标数组
};

class GRO
{
public:
    GRO(std::string file_path)
    {
        this->file_path = file_path;
        this->read_gro();
    }
    std::vector<std::string> rename_vector;                                         // 存储残基名的数组
    std::vector<int> rename_number_vector;                                          // 存储残基个数的数组
    std::string file_path;                                                          // gro文件路径
    std::map<int, GRO_reside> dict;                                                 // 存储gro中信息的字典
    int atom_number;                                                                // gro中的原子数
    std::string dimension;                                                          // gro中最后一行信息
    void read_gro();                                                                // 读取gro文件
    int resname_number_index(std::string s);                                        // 返回残基名第一个非数字的字符的索引
    void replace_resname(int start, int end, std::string resname);                  // 替换残基名
    void replace_atom_name(int start, int end, std::vector<std::string> atom_name); // 替换原子名
    void write_gro(std::string file_path);                                          // 输出gro文件信息
    std::string Trim(std::string s);                                                // 去除字符串前后的空格
    std::vector<std::string> splitString(std::string s);                            // 根据空格将字符串进行分割
    std::string Delete_prefix_number(std::string s);                                // 去除字符串前面的数字
    void Show_resname_inf();                                                        // 显示残基数量的相关信息
};

std::string GRO::Trim(std::string s)
{
    if (s.empty())
        return s;
    s.erase(0, s.find_first_not_of(" ")); // 删除字符
    s.erase(s.find_last_not_of(" ") + 1);
    return s;
}

std::string GRO::Delete_prefix_number(std::string s)
{
    return s.substr(this->resname_number_index(s), s.size() - this->resname_number_index(s));
}

std::vector<std::string> GRO::splitString(std::string s)
{
    s = this->Trim(s);
    std::vector<std::string> result;
    int i, flag = 0;
    std::string result_str = "";
    for (i = 0; i < s.size(); i++)
    {
        std::string s_tmp(1, s[i]); // 把char转换为string
        if (i == 0)
            result_str += s_tmp;
        else
        {
            if ((s_tmp == " ") && (flag == 0))
            {
                flag = 1;
                result.push_back(result_str);
                result_str = "";
                continue;
            }
            if ((s_tmp == " ") && (flag == 1))
            {
                continue;
            }
            result_str += s_tmp;
            flag = 0;
            if (i == (s.size() - 1))
                result.push_back(result_str);
        }
    }
    return result;
}

int GRO::resname_number_index(std::string s) // 返回残基名第一个非数字的字符的索引
{
    int i;
    for (i = 0; i < s.size(); i++)
        if (!(s[i] >= '0' && s[i] <= '9'))
            break;
    return i;
}

void GRO::read_gro()
{
    std::ifstream in(this->file_path);
    std::string line;
    std::getline(in, line);         // 读第一行，舍弃
    std::getline(in, line);         // 第二行为原子数
    line = this->Trim(line);        // 去除左右两侧的空格
    this->atom_number = stoi(line); // 将string转换为int
    std::string resname_tmp = " ";
    int resname_index = 0;
    std::vector<std::string> line_list;

    for (int i = 0; i < this->atom_number; i++)
    {
        std::getline(in, line);
        line_list = this->splitString(line);

        if ((resname_tmp == " ") || (line_list[0] != resname_tmp)) // 写入一个新残基的信息
        {
            resname_index++;
            resname_tmp = line_list[0];
            GRO_reside G = GRO_reside();
            // G.resname = resname_tmp.substr(this->resname_number_index(resname_tmp), resname_tmp.size() - this->resname_number_index(resname_tmp));
            G.resname = this->Delete_prefix_number(resname_tmp);
            std::vector<std::string> atom_tmp;
            atom_tmp.push_back(line_list[1]);
            G.atom_name = atom_tmp;
            std::vector<coordinate> coor;
            coordinate c = coordinate();
            c.x = stod(line_list[3]);
            c.y = stod(line_list[4]);
            c.z = stod(line_list[5]);
            coor.push_back(c);
            G.coor_vector = coor;
            this->dict.insert(std::pair<int, GRO_reside>(resname_index, G));
        }
        else
        {
            this->dict[resname_index].atom_name.push_back(line_list[1]);
            coordinate c = coordinate();
            c.x = stod(line_list[3]);
            c.y = stod(line_list[4]);
            c.z = stod(line_list[5]);
            this->dict[resname_index].coor_vector.push_back(c);
        }
    }
    std::getline(in, line);
    this->dimension = line;
}

void GRO::replace_resname(int start, int end, std::string resname)
{
    for (int i = start; i <= end; i++)
        this->dict[i].resname = resname;
}

void GRO::replace_atom_name(int start, int end, std::vector<std::string> atom_name)
{
    for (int i = start; i <= end; i++)
        this->dict[i].atom_name = atom_name;
}

void GRO::write_gro(std::string file_path)
{
    std::ofstream outputFile;
    outputFile.open(file_path);
    if (outputFile.is_open())
    {
        outputFile << "Built with modGro" << std::endl;
        outputFile << " " << this->atom_number << std::endl;
        int atom_index = 1, i, j;
        for (i = 0; i < this->dict.size(); i++)
        {
            for (j = 0; j < this->dict[i + 1].atom_name.size(); j++)
            {
                outputFile << std::right << std::setw(5) << std::to_string(i + 1) << std::left << std::setw(3) << this->dict[i + 1].resname << std::right << std::setw(7) << this->dict[i + 1].atom_name[j] << std::right << std::setw(5) << atom_index << std::right << std::setw(8) << std::fixed << std::setprecision(3) << this->dict[i + 1].coor_vector[j].x << std::right << std::setw(8) << this->dict[i + 1].coor_vector[j].y << std::right << std::setw(8) << this->dict[i + 1].coor_vector[j].z << std::endl;
                atom_index++;
            }
        }
        outputFile << this->dimension << std::endl;
    }
}

void GRO::Show_resname_inf()
{
    std::string resname_tmp1 = this->dict[1].resname;
    this->rename_vector.push_back(resname_tmp1);
    int resname_number_tmp = 0;
    for (int i = 1; i <= this->dict.size(); i++)
    {
        if (this->dict[i].resname == resname_tmp1)
            resname_number_tmp++;
        else
        {
            this->rename_vector.push_back(this->dict[i].resname);
            resname_tmp1 = this->dict[i].resname;
            this->rename_number_vector.push_back(resname_number_tmp);
            resname_number_tmp = 1;
        }
    }
    this->rename_number_vector.push_back(resname_number_tmp);
    std::cout << std::endl;
    for (int i = 0; i < this->rename_number_vector.size(); i++)
        std::cout << this->rename_vector[i] << ": " << this->rename_number_vector[i] << std::endl;
    std::cout << std::endl;
    this->rename_number_vector.clear();
    this->rename_vector.clear();
}

int main()
{
    std::cout << "modGro: A tool for modifying gro file" << std::endl;
    std::cout << "Version 1.0, release date: 2024-Dec-4" << std::endl;
    std::cout << "Programmed by Jian Zhang (jian_zhang@cug.edu.cn)" << std::endl
              << std::endl;
    std::cout << "Please input the file path of .gro" << std::endl;
    std::string file_path, input_index;
    std::cin >> file_path;
    GRO gro_object = GRO(file_path);
    std::cout << std::endl;
    std::cout << "The number of atoms: " << gro_object.atom_number << std::endl;
    std::cout << "The number of residues: " << gro_object.dict.size() << std::endl;
    while (true)
    {
        gro_object.Show_resname_inf();
        std::cout << "0 Save" << std::endl
                  << "1 Change residue name" << std::endl
                  << "2 Change atom name" << std::endl
                  << "q Exit the program" << std::endl;
        std::cin >> input_index;
        if (input_index == "0")
        {
            gro_object.write_gro("./fix.gro");
            break;
        }
        else if (input_index == "1")
        {
            int start, end;
            std::string resname_change;
            std::cout << "Please enter the starting value (from 1) of the serial number of the residue whose name is to be changed" << std::endl;
            std::cin >> start;
            std::cout << "Please enter the ending value for the serial number of the residue for which the name change is required" << std::endl;
            std::cin >> end;

            if ((start <= end) && (start > 0) && (end <= gro_object.dict.size()))
            {
                std::cout << "Please enter the changed residue name" << std::endl;
                std::cin >> resname_change;
                gro_object.replace_resname(start, end, resname_change);
            }
            else
            {
                std::cout << "Invalid input" << std::endl;
                continue;
            }
        }
        else if (input_index == "2")
        {
            int start, end, i;
            std::string atom_name_change;
            std::vector<std::string> atom_name;
            std::cout << "Please enter the starting value (from 1) of the serial number of the residue whose atomic name needs to be changed." << std::endl;
            std::cin >> start;
            std::cout << "Please enter the ending value for the serial number of the residue whose atomic name needs to be changed." << std::endl;
            std::cin >> end;
            if ((start <= end) && (start > 0) && (end <= gro_object.dict.size()))
            {
                std::cout << "The number of atoms in these residues: " << gro_object.dict[start].atom_name.size() << std::endl
                          << "Please enter the changed atomic name" << std::endl;
                for (i = 0; i < gro_object.dict[start].atom_name.size(); i++)
                {
                    std::cin >> atom_name_change;
                    atom_name.push_back(atom_name_change);
                }
                gro_object.replace_atom_name(start, end, atom_name);
            }
            else
                std::cout << "Invalid input" << std::endl;
        }
        else if (input_index == "q")
            break;
        else
            std::cout << "Invalid input" << std::endl;
    }

    return 0;
}
